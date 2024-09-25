from django.urls import path

from . import views

urlpatterns = [
    path("en/topics/", views.ENTopicsView.as_view(), name="en-topics-page"),
    path("en/<slug:slug>", views.ENStartingPageView.as_view(), name="en-starting-page"),
    path("en/starting_request/<slug:slug>", views.ENStartingPageInitialRequest.as_view(), name="en_speaking_starting_request"),
    path("en/request/", views.EnspeakingRequest.as_view(), name="en_speaking_request"),
]
