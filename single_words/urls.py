from django.urls import path

from . import views

urlpatterns = [
    path("overview/", views.single_word_pick_category.as_view(), name="single_word_pick_category"),
    path("word_pick/", views.single_word_pick_word.as_view(), name="single_word_pick_word"),
    path("training/", views.training_view.as_view(), name="single_words_training"),
    path("training_solution", views.training_solution_view.as_view(), name="single_words_training_solution")
]
