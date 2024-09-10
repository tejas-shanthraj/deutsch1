import re
import epitran
# Model
from .models import Sentences, Words

from django.core.paginator import Paginator

epi = epitran.Epitran('deu-Latn')

import random

# Practice pronouncing sentences
def get_sentence( limit=5, offset=0):

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
    if (data['type'] == "sentence"):
        try:
            db_data = Sentences.objects.filter(id=data['sentence_id']).values('sentence', 'ipa').first()  # Fetching the sentence and IPA from the database

            if not db_data:
                return {'error': 'Sentence not found', 'status': 404}
        except Sentences.DoesNotExist:
            return {'error': 'Sentence not found', 'status': 404}
        
        original_sentence = re.sub(r'[^\w\s]', '', db_data['sentence'])
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
        
        original_sentence = re.sub(r'[^\w\s]', '', db_data['word'])
        original_ipa = db_data['ipa']

        recorded_ipa = epi.transliterate(data['transcript'])

        result = compare_phonetics(original_ipa, recorded_ipa, original_sentence.lower().split(), data['transcript'].lower().split())

        return {
            "correctness": result['correctness'],
            "errors": result['errors']
        }

def compare_phonetics(original_phonetic, recorded_phonetic, original_words, recorded_words):

    correct_phonetics = [i for i in original_phonetic.split() for j in recorded_phonetic.split() if i == j]
    incorrect_phonetics = list(set(original_phonetic.split()).difference(recorded_phonetic.split()))

    original_words = list(map(str.lower, original_words))
    recorded_words = list(map(str.lower, recorded_words))

    correct_words = [i for i in original_words for j in recorded_words if i.lower() == j.lower()]
    
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