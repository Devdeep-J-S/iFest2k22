from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.iohome, name='iohome'),
    path('puzzles/<slug:slug>', views.puzzle, name='puzzle'),
]