from django.urls import path

from . import views

urlpatterns = [
    # Voice Assistant
    path('ai/', views.VoiceAssistantStartPageView.as_view(), name='assistant_practice'),
    path('transcribe-audio/', views.transcribe_audio_view, name='transcribe_audio'),
]