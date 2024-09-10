from django.urls import path

from . import views

urlpatterns = [
    path("ru/topics/", views.RUTopicsView.as_view(), name="practice-ru-topics-page"),
    path("en/topics/", views.ENTopicsView.as_view(), name="practice-en-topics-page"),
    path("ru/<slug:slug>", views.RUStartingPageView.as_view(), name="practice-ru-starting-page"),
    path("en/<slug:slug>", views.ENStartingPageView.as_view(), name="practice-en-starting-page"),
    path("ru/starting_request/<slug:slug>", views.RUStartingPageInitialRequest.as_view(), name="practice-ru_speaking_starting_request"),
    path("en/starting_request/<slug:slug>", views.ENStartingPageInitialRequest.as_view(), name="practice-en_speaking_starting_request"),
    path("ru/request/", views.RupracticingRequest.as_view(), name="practice-ru_speaking_request"),
    path("en/request/", views.EnpracticingRequest.as_view(), name="practice-en_speaking_request"),
]
