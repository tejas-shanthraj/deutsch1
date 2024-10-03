from django.shortcuts import render
from django.views import View
# from rest_framework.views import APIView
from django.http import HttpResponse
import json

from .helpers import chat_helper
from .models import PracticingSituation


class ENTopicsView(View):
    def get(self, request):
        situations = PracticingSituation.objects.filter(lang = "en-US")
        print(f'From backend {situations}')
        context = {
            "situations": situations,
            "lang": "en-US",
        }
        return render(request, "practicing/situations.html", context)


class ENStartingPageView(View):
    def get(self, request, slug):
        situation = PracticingSituation.objects.get(id = slug)
        situation_id = situation.id
        
        context = {
            "situation_id": situation_id,
            "situation": situation,
            "lang": "en-US",
        }
        return render(request, "practicing/training.html", context)

        
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