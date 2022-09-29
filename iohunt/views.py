import re
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#from ..iFest_2021.models import Registration
from .models import *
import datetime

# Create your views here.

@login_required(login_url='login_page')
def iohome(request):
    #q = Registration.filter(event='IOHunt')
    #if q.objects.get(userProfile=request.user) is None:
    #    return redirect('$iohunteventpage$')
    if request.method == "POST":
        try:
            player = Player.objects.get(userProfile=request.user)
            if player.status == 'E':
                return render(request, 'ended.html')
            puzzle = Puzzle.objects.get(name='start')
            return redirect('puzzle', slug=puzzle.link)
        except:
            now = datetime.datetime.now()
            player = Player(userProfile=request.user, status='S', startTime=now)
            player.save()
            puzzle = Puzzle.objects.get(name='start')
            return redirect('puzzle', slug=puzzle.link)
    return render(request, 'iohome.html')

@login_required(login_url='login_page')
def puzzle(request, slug):
    player = Player.objects.get(userProfile=request.user)
    now = datetime.datetime.now()
    if player is None:
        return redirect('iohome')
    if player.status != 'S':
        # Test completed.
        return redirect('iohome')
    try: 
        puzzle = Puzzle.objects.get(link=slug)
    except:
        return render(request, 'lost.html')
    if request.method == "POST":
        if request.POST['ans'] == puzzle.Data['answer']:
            messages.info(request, "Correct Answer!")
            if puzzle.name == 'end':
                player.endTime = now
                player.status = 'E'
                player.save()
                return render(request, 'ended.html')
        else:
            messages.info(request, "Incorrect Answer. Try Again!")

    return render(request, 'puzzle.html', {'puzzle':puzzle})