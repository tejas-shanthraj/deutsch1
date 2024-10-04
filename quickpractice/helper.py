import os
import re
import random
import epitran
from .models import Sentences, Words
from django.core.paginator import Paginator
import azure.cognitiveservices.speech as speechsdk

epi = epitran.Epitran('deu-Latn')

# Practice pronouncing sentences
def get_sentence( limit=5, offset=0):
    """
    Fetch sentences frm the database based on the provided limit and offset values, else use the default values.
    Creates a list and returns the values.
    """

    data = Sentences.objects.all()[offset:offset + limit]

    total = Sentences.objects.count()

    remaining = total - (offset + limit) if total > (offset + limit) else 0

    next_offset = offset + limit if remaining > 0 else None

    sentences_data = [
        {
            'id': sentence.id,
            'sentence': re.sub(r"'", "9999", sentence.sentence),
            'en_translation': re.sub(f"'", "9999", sentence.en_translation),
            'lang': sentence.lang,
            'phonetic': re.sub(r"'", "9999", sentence.phonetic),
            'ipa': re.sub(r"'", "9999", sentence.ipa),
            'category': sentence.category,
            'difficulty': sentence.difficulty
        } for sentence in data
    ]

    return {
        'total': total,
        'remaining': remaining,
        'limit': limit,
        'next': next_offset,
        'data': sentences_data
    }

def get_word(limit=5, offset=0):
    """
    Fetch words frm the database based on the provided limit and offset values, else use the default values.
    Creates a list and returns the values.
    """

    data = Words.objects.all()[offset:offset + limit]

    total = Words.objects.count()

    remaining = total - (offset + limit) if total > (offset + limit) else 0

    next_offset = offset + limit if remaining > 0 else None

    words_data = [
        {
            'id': word.id,
            'word': re.sub(r"'", "9999", word.word),
            'en_translation': re.sub(f"'", "9999", word.en_translation),
            'lang': word.lang,
            'phonetic': re.sub(r"'", "9999", word.phonetic),
            'ipa': re.sub(r"'", "9999", word.ipa),
            'category': word.category,
            'difficulty': word.difficulty
        } for word in data
    ]

    return {
        'total': total,
        'remaining': remaining,
        'limit': limit,
        'next': next_offset,
        'data': words_data
    }

def check_score(data):
    """
    Based on the data type this functions fetches the original IPA and Phoneme from the database,
    which is then used to compare the correctness between the user's response and original response.
    Returns a list of error words and correctness percentage.
    """
    if (data['type'] == "sentence"):
        try:
            db_data = Sentences.objects.filter(id=data['sentence_id']).values('sentence', 'ipa').first()  # Fetching the sentence and IPA from the database

            if not db_data:
                return {'error': 'Sentence not found', 'status': 404}
        except Sentences.DoesNotExist:
            return {'error': 'Sentence not found', 'status': 404}
        
        original_sentence = db_data['sentence']
        original_ipa = db_data['ipa']

        recorded_ipa = epi.transliterate(data['transcript'])

        result = compare_phonetics(original_ipa, recorded_ipa, original_sentence.split(), data['transcript'].split())

        return {
            "correctness": result['correctness'],
            "errors": result['errors']
        }
    
    elif (data['type'] == "word"):
        try:
            db_data = Words.objects.filter(id=data['word_id']).values('word', 'ipa').first()  # Fetching the sentence and IPA from the database

            if not db_data:
                return {'error': 'Word not found', 'status': 404}
        except Words.DoesNotExist:
            return {'error': 'Word not found', 'status': 404}
        
        original_sentence = db_data['word']
        original_ipa = db_data['ipa']

        recorded_ipa = epi.transliterate(data['transcript'])

        result = compare_phonetics(original_ipa, recorded_ipa, original_sentence.lower().split(), data['transcript'].lower().split())

        return {
            "correctness": result['correctness'],
            "errors": result['errors']
        }

def compare_phonetics(original_phonetic, recorded_phonetic, original_words, recorded_words):
    """
    Compares original phonetics and words, contains a logic to calculate the score.
    Returns correctness percentage and list of errors.
    """

    correct_phonetics = [i for i in original_phonetic.split() for j in recorded_phonetic.split() if i == j]
    incorrect_phonetics = list(set(original_phonetic.split()).difference(recorded_phonetic.split()))

    correct_words = [i for i in original_words for j in recorded_words if i == j]
    
    incorrect_words = list(set(original_words).difference(recorded_words))
    # Incorrect words set 1
    inw_set1 = incorrect_words
    inw_set1.sort(key=original_words.index)
    
    incorrect_words1 = list(set(recorded_words).difference(original_words))
    # Incorrect words set 2
    inw_set2 = incorrect_words1
    inw_set2.sort(key=recorded_words.index)
    
    print(f'After \n OW - {original_words} \n RW - {recorded_words} \n CW - {correct_words}\n IW - {incorrect_words}\n IW1 - {incorrect_words1}')

    
    errors = []
    
    total_words = len(original_words)
    correct_words = 0

    for i in range(len(inw_set1)):
        if i < len(inw_set2):
            errors.append({
                'original': inw_set1[i],
                'recorded': inw_set2[i]
            })
        else:
            errors.append({
                'original': inw_set1[i],
                'recorded': "N/A"
            })

    correctness = ((total_words - len(incorrect_words)) / total_words) * 100 if total_words > 0 else 0
    # print(f'\n\n\n Errors: {errors}')
    return {'correctness': round(correctness, 2), 'errors': errors}

# def check_score1(data):
#     print(data)
#     # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
#     speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
#     speech_config.speech_recognition_language="de-DE"

#     audio_config = speechsdk.audio.AudioConfig(use_default_microphone=False)
#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

#     pronunciationConfig = speechsdk.PronunciationAssessmentConfig(
#         data['reference_text'], 
#         speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
#         speechsdk.PronunciationAssessmentGranularity.Phoneme,
#         False
#     )
#     pronunciationConfig.enable_prosody_assessment() 
#     pronunciationConfig.enable_content_assessment_with_topic("greeting")
    
#     print(pronunciationConfig)

#     print("Speak into your microphone.")
#     speech_recognition_result = speech_recognizer.recognize_once_async().get()

#     if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
#         print("Recognized: {}".format(speech_recognition_result.text))
#     elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
#         print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
#     elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
#         cancellation_details = speech_recognition_result.cancellation_details
#         print("Speech Recognition canceled: {}".format(cancellation_details.reason))
#         if cancellation_details.reason == speechsdk.CancellationReason.Error:
#             print("Error details: {}".format(cancellation_details.error_details))
#             print("Did you set the speech resource key and region values?")