from django.urls import path

from . import views

urlpatterns = [
    # Sentence API
    path('sentences/', views.SentenceStartPageView.as_view(), name='sent_practice'),
    path('score/', views.get_score, name='score'),

    # Word API
    path('words/', views.WordStartPageView.as_view(), name='word_practice'),
]