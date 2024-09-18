import os
import azure.cognitiveservices.speech as speechsdk

from config import SPEECH_KEY, SPEECH_REGION

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


    # The pronunciation assessment result as a Speech SDK object
    pronunciation_assessment_result = speechsdk.PronunciationAssessmentResult(speech_recognition_result)

    # The pronunciation assessment result as a JSON string
    pronunciation_assessment_result_json = speech_recognition_result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)


    print(pronunciation_assessment_result)
    print("\n---------\n")
    print(pronunciation_assessment_result_json)
    print("\n---------\n")
    print(pronunciation_assessment_result.accuracy_score)
    print(pronunciation_assessment_result.completeness_score)
    print(pronunciation_assessment_result.content_assessment_result)
    print(pronunciation_assessment_result.fluency_score)
    print(pronunciation_assessment_result.pronunciation_score)
    print(pronunciation_assessment_result.words)

    return pronunciation_assessment_result_json


import json

def get_dummy_eval(reference_text):
    # file_path = 'single_words\\temp.json'
    # with open(file_path, 'r') as file:
    #     content = json.load(file)
    # return content
    eval = recognize_from_microphone(reference_text)
    return eval

def get_feedback(reference_text):
    eval = recognize_from_microphone(reference_text)
    return eval









