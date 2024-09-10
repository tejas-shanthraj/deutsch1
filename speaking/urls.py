from django.urls import path

from . import views

urlpatterns = [
    path("ru/topics/", views.RUTopicsView.as_view(), name="ru-topics-page"),
    path("en/topics/", views.ENTopicsView.as_view(), name="en-topics-page"),
    path("ru/<slug:slug>", views.RUStartingPageView.as_view(), name="ru-starting-page"),
    path("en/<slug:slug>", views.ENStartingPageView.as_view(), name="en-starting-page"),
    path("ru/starting_request/<slug:slug>", views.RUStartingPageInitialRequest.as_view(), name="ru_speaking_starting_request"),
    path("en/starting_request/<slug:slug>", views.ENStartingPageInitialRequest.as_view(), name="en_speaking_starting_request"),
    path("ru/request/", views.RuspeakingRequest.as_view(), name="ru_speaking_request"),
    path("en/request/", views.EnspeakingRequest.as_view(), name="en_speaking_request"),
]
