from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('<slug:quizname>', views.quizhome, name='quizhome'),
    path('<slug:quizname>/start', views.quiz, name='quiz'),
]