from django.shortcuts import render
from django.views import View
# from rest_framework.views import APIView
from django.http import HttpResponse
import json

from .helpers import chat_helper
from .models import PracticingSituation

class RUTopicsView(View):
    def get(self, request):
        situations = PracticingSituation.objects.filter(lang = "ru-RU")
        context = {
            "situations": situations,
            "lang": "ru-RU",
        }
        return render(request, "practicing/index_ru.html", context)
    
class ENTopicsView(View):
    def get(self, request):
        situations = PracticingSituation.objects.filter(lang = "en-US")
        context = {
            "situations": situations,
            "lang": "en-US",
        }
        return render(request, "practicing/index_en.html", context)

class RUStartingPageView(View):
    def get(self, request, slug):
        situation = PracticingSituation.objects.get(id = slug)
        situation_id = situation.id
        
        context = {
            "situation_id": situation_id,
            "situation": situation,
            "lang": "ru-RU",
        }
        return render(request, "practicing/situation_ru.html", context)
    
class ENStartingPageView(View):
    def get(self, request, slug):
        situation = PracticingSituation.objects.get(id = slug)
        situation_id = situation.id
        
        context = {
            "situation_id": situation_id,
            "situation": situation,
            "lang": "en-US",
        }
        return render(request, "practicing/situation_en.html", context)

class RUStartingPageInitialRequest(View):
    def get(self, request, slug):
        print('request: ', request)
        if slug:
            situation = PracticingSituation.objects.get(id = slug)
            starting_message, conv_id = chat_helper.GetStartingMessageRU(situation)
            response = {
               'starting_message': starting_message, 
               'conv_id': conv_id,
            }
            return HttpResponse(json.dumps(response), status = 200 )
        else:
            return HttpResponse(json.dumps(False), status = 400 )
        
class ENStartingPageInitialRequest(View):
    def get(self, request, slug):
        print('request: ', request)
        if slug:
            situation = PracticingSituation.objects.get(id = slug)
            starting_message, conv_id = chat_helper.GetStartingMessageEN(situation)
            response = {
               'starting_message': starting_message, 
               'conv_id': conv_id,
            }
            return HttpResponse(json.dumps(response), status = 200 )
        else:
            return HttpResponse(json.dumps(False), status = 400 )
    
class RupracticingRequest(View):
    def post(self, request):
        print('request: ', request)
        # data = request.POST.get('data', False)
        data = json.loads(request.body.decode('utf-8'))
        print('data: ', data)
        if data:
            # print('data: ', data)
            result = chat_helper.GetTeacherResponseRU(data['message'], data['conv_id'])
            response = {
               'new_message': result, 
            }
            return HttpResponse(json.dumps(response), status = 200 )
        else:
            return HttpResponse(json.dumps(False), status = 400 )
    
class EnpracticingRequest(View):
    def post(self, request):
        print('request: ', request)
        # data = request.POST.get('data', False)
        data = json.loads(request.body.decode('utf-8'))
        print('data: ', data)
        if data:
            # print('data: ', data)
            result = chat_helper.GetTeacherResponseEN(data['message'], data['conv_id'])
            response = {
               'new_message': result, 
            }
            return HttpResponse(json.dumps(response), status = 200 )
        else:
            return HttpResponse(json.dumps(False), status = 400 )