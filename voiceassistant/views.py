import os
import json
import logging
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from langchain.memory import ConversationBufferMemory
from voiceassistant.utils import transcribe_audio, get_response_llm, load_whisper
from dotenv import load_dotenv
import tempfile
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Create your views here.
logger = logging.getLogger(__name__)
# Load environment variables from .env file
load_dotenv()

# Initialize Whisper model
model = load_whisper()

# Home page view
class VoiceAssistantStartPageView(View):
    def get(self, request):
        return render(request, 'index.html')
    

from langdetect import detect, DetectorFactory
from django.core.files.storage import default_storage

@csrf_exempt
def transcribe_audio_view(request):
    if request.method == 'POST':
        # Get scenario
        scenario = request.POST.get('scenario')
        if not scenario:
            return JsonResponse({'error': 'Scenario is required'}, status=400)
        
        # Handle audio file
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return JsonResponse({'error': 'Audio file is required'}, status=400)


        # Save the file
        temp_file_name = 'temp_audio.wav'
        temp_file_path = os.path.join(f'{ROOT_DIR}/media', temp_file_name)

        print(f'temp_file_path {temp_file_path} - os.path - {os.path.basename}')

        with default_storage.open(temp_file_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        text = transcribe_audio(model, temp_file_path)
        print(f'Text - now - {text}')
        # os.remove(temp_file_path)
        
        # For testing purpose - Detect language
        # try:
        #     lang = detect(text)
        #     print(f'LANGUAGE - {lang}')
        # except Exception as e:
        #     return JsonResponse({'error': f'Language detection failed: {e}'}, status=500)

        # if lang != 'de':
        #     return JsonResponse({'error': 'The recorded speech is not in German'}, status=400)

        memory = ConversationBufferMemory(memory_key="chat_history")
        groq_api_key = os.getenv('GROQ_API_KEY')  # Set your API key here

        if not groq_api_key:
            return JsonResponse({'error': 'GROQ_API_KEY is not set'}, status=400)

        prompt_type = "wlan" if scenario == "WLAN Troubleshooting" else "hotel"
        response_llm = get_response_llm(user_question=text, memory=memory, groq_api_key=groq_api_key, prompt_type=prompt_type)
        print(f'Response generated from LLM - {response_llm}')
        
        # Generate audio response (if required) only for backend audio play purpose.
        # assistant_audio_url = play_text_to_speech(response_llm) # This line plays thee audio clip or the response clip from the backend
        # assistant_audio_url = default_storage.url(temp_file_path)  # Use `default_storage.url` to get the correct URL
        # print(assistant_audio_url)

        return JsonResponse({'customer_text': text, 
                             'assistant_response': response_llm,
                             'assistant_audio_url': '', # assistant_audio_url
                             })

    return JsonResponse({'error': 'Invalid request method'}, status=405)