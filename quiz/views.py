import re
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#from ..ifest2022.models import Registration
from .models import *
import datetime

# Create your views here.

@login_required(login_url='login_page')
def quizhome(request, quizname):
    #q = Registration.filter(event='IOHunt')
    #if q.objects.get(userProfile=request.user) is None:
    #    return redirect('$iohunteventpage$')
    if request.method == "POST":
        try:
            Qplayer.objects.get(userProfile=request.user, quizName=quizname)
            if player.status == 'E':
                return render(request, 'qended.html')
            return redirect('quiz', quizname=quizname)
        except:
            now = datetime.datetime.now()
            player = Qplayer(userProfile=request.user, quizName=quizname, status='S', startTime=now, score=0)
            player.save()
            return redirect('quiz', quizname=quizname)
    return render(request, 'quizhome.html', {'quizname':quizname})


@login_required(login_url='login_page')
def quiz(request, quizname):
    player = Qplayer.objects.get(userProfile=request.user, quizName=quizname)
    now = datetime.datetime.now()
    if player is None:
        return redirect('quizhome')
    if player.status != 'S':
        # Test completed.
        return redirect('quizhome', quizname=quizname)
    quiz = Quiz.objects.get(name=quizname)
    if request.method == "POST":
        if quiz.mcq is not None:
            for q in quiz.mcq:
                if request.POST[q] == quiz.mcq[q]['answer']:
                    player.score += int(quiz.mcq[q]['score'])
        if quiz.saq is not None:
            for q in quiz.saq:
                if request.POST[q] == quiz.saq[q]['answer']:
                    player.score += int(quiz.saq[q]['score'])
        player.endTime = now
        player.status = 'E'
        player.save()
        return render(request, 'qended.html')
    return render(request, 'quiz.html', {'quiz':quiz})

