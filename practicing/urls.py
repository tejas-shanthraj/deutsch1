from django.urls import path

from . import views

urlpatterns = [
    path("en/topics/", views.ENTopicsView.as_view(), name="practice-en-topics-page"),
    path("en/<slug:slug>", views.ENStartingPageView.as_view(), name="practice-en-starting-page"),
    path("en/starting_request/<slug:slug>", views.ENStartingPageInitialRequest.as_view(), name="practice-en_speaking_starting_request"),
    path("en/request/", views.EnpracticingRequest.as_view(), name="practice-en_speaking_request"),
]
