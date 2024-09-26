from django.shortcuts import render, redirect
from django.views import View
# from rest_framework.views import APIView
from django.http import HttpResponse
import json

from .models import SingleWordsSituation, SingleWordsVideos

# /overview
class single_word_pick_category(View):
    def get(self, request):
        
        situations = SingleWordsVideos.objects.all()
        
        context = {
            "situations": situations
        }
        return render(request, "single_words/training_pick_category.html", context)


class single_word_pick_word(View):
    def get(self, request):
        ID_NOT_SET_VALUE = "ID_NOT_SET"
        sound_type = request.GET.get("sound_type", ID_NOT_SET_VALUE)

        if sound_type == ID_NOT_SET_VALUE:
            response = redirect('/single_words/overview/')
            return response
        
        info_video_url = SingleWordsVideos.objects.filter(sound_type__iexact=sound_type)
        sound_type_id = info_video_url[0].id
        info_video_url = info_video_url[0].url

        situations = SingleWordsSituation.objects.filter(sound_type=sound_type_id)
        
        
        context = {
            "situations": situations,
            "sound_type": sound_type,
            "info_video_url": info_video_url,
        }
        return render(request, "single_words/training_pick_word.html", context)

import random
class training_view(View):
    def get(self, request):
        ID_NOT_SET_VALUE = "ID_NOT_SET"
        word_id = request.GET.get("word_id", ID_NOT_SET_VALUE)

        if word_id == ID_NOT_SET_VALUE:
            response = redirect('/single_words/overview/')
            return response
        
        if word_id == "random":
            sound_type = request.GET.get("sound_type", ID_NOT_SET_VALUE)

            if sound_type == ID_NOT_SET_VALUE:
                response = redirect('/single_words/overview/')
                return response


            info_video_url = SingleWordsVideos.objects.filter(sound_type__iexact=sound_type)
            sound_type = info_video_url[0].id
            situations = list(SingleWordsSituation.objects.filter(sound_type=sound_type))
            situations = random.sample(situations, 1)

            word_id = situations[0].id


        word = SingleWordsSituation.objects.get(id = word_id).word
        image = SingleWordsSituation.objects.get(id = word_id).image
        sound_type = SingleWordsSituation.objects.get(id = word_id).sound_type

        context = {
            "word": word,
            "word_id": word_id,
            "image": image,
            "sound_type": sound_type,
        }
        return render(request, "single_words/training.html", context)
    
#from .logic import get_dummy_eval
from .config import SPEECH_KEY, SPEECH_REGION
import os
import azure.cognitiveservices.speech as speechsdk
import json
class training_solution_view(View):
    def get(self, request, *args, **kwargs):
        ID_NOT_SET_VALUE = "ID_NOT_SET"
        word_id = request.GET.get("word_id", ID_NOT_SET_VALUE)

        if word_id == ID_NOT_SET_VALUE:
            response = redirect('/single_words/overview/')
            return response
        
        word = SingleWordsSituation.objects.get(id = word_id).word
        image = SingleWordsSituation.objects.get(id = word_id).image
        sound_type = SingleWordsSituation.objects.get(id = word_id).sound_type
        

        total_accuracy_score = 0
        syllable_scores = []
        try:
            eval = recognize_from_microphone(reference_text = word)
            eval = json.loads(eval)

            total_accuracy_score = eval['NBest'][0]["PronunciationAssessment"]["AccuracyScore"] 
            
            syllable_scores = []
            syllables = eval['NBest'][0]["Words"][0]["Syllables"] 
            for syllable in syllables:
                accuracy_score = syllable['PronunciationAssessment']['AccuracyScore']
                syllable_scores.append(accuracy_score)
        except:
            total_accuracy_score = 0
            syllable_scores = [0]

        # get syllables stored in db
        syllables = str(SingleWordsSituation.objects.get(id = word_id).syllables)
        syllables = syllables.split(",")
        n_syllables = len(syllables)

        # in case azure returns a different syllable count
        syllables_difference = n_syllables -len(syllable_scores)
        if syllables_difference > 0:
            for i in range(syllables_difference):
                syllable_scores.append(accuracy_score)

        syllables_and_scores = zip(syllables, syllable_scores)    

        context = {
            "word": word,
            "word_id": word_id,
            "image": image,
            "accuracy_score": total_accuracy_score,
            "n_syllables": n_syllables,
            "syllables_and_scores": syllables_and_scores,
            "sound_type": sound_type,
        }

        return render(request, "single_words/training_solution.html", context)
    

def recognize_from_microphone(reference_text):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_recognition_language="de-DE"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    
    pronunciation_assessment_config = speechsdk.PronunciationAssessmentConfig( 
        reference_text=reference_text, 
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark, 
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme, 
        enable_miscue=False) 

    pronunciation_assessment_config.apply_to(speech_recognizer)
    speech_recognition_result = speech_recognizer.recognize_once()


    # The pronunciation assessment result as a JSON string
    pronunciation_assessment_result_json = speech_recognition_result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
    print(pronunciation_assessment_result_json)

    return pronunciation_assessment_result_json


