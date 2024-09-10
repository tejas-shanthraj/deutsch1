import json
import logging
from django.views import View
from django.shortcuts import render
from quickpractice.helper import get_sentence, check_score, get_word
from django.http import JsonResponse, HttpResponse

# Create your views here.
logger = logging.getLogger(__name__)

class SentenceStartPageView(View):
    def get(self, request):
        limit = int(request.GET.get('limit', 5))  # Default limit is 5
        offset = int(request.GET.get('offset', 0))

        fetch_sentences = get_sentence(limit, offset)
        context = {
            'total': fetch_sentences['total'],
            'remaining': fetch_sentences['remaining'],
            'limit': fetch_sentences['limit'],
            'next': fetch_sentences['next'],
            'data': fetch_sentences['data']
        }
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            logger.debug("AJAX request detected.")
            return JsonResponse(context)
        
        if request.GET.get('ajax') == 'true':
            print('VAlue')
            return JsonResponse(context)
        
        logger.debug("Non-AJAX request detected.")
        print("Non-AJAX request detected.")
        return render(request, "sentence.html", context)

class WordStartPageView(View):
    def get(self, request):
        limit = int(request.GET.get('limit', 5))
        offset = int(request.GET.get('offset', 5))

        fetch_words = get_word(limit, offset)
        context = {
            'total': fetch_words['total'],
            'remaining': fetch_words['remaining'],
            'limit': fetch_words['limit'],
            'next': fetch_words['next'],
            'data': fetch_words['data']
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            logger.debug("AJAX request detected.")
            return JsonResponse(context)
        
        if request.GET.get('ajax') == 'true':
            print('VAlue')
            return JsonResponse(context)
        
        logger.debug("Non-AJAX request detected.")
        print("Non-AJAX request detected.")
        return render(request, "word.html", context)

def get_score(request):
    if request.method == 'POST':
        
        result = check_score(json.loads(request.body))

    return JsonResponse(result)