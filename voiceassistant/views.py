import json
import logging
from django.views import View
from django.shortcuts import render
from voiceassistant import 
from django.http import JsonResponse, HttpResponse

# Create your views here.
logger = logging.getLogger(__name__)

class VoiceAssistantStartPageView(View):
    def get(self, request):
        return render(request, 'index.html')

def ai_eval():