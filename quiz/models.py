import json
from django.db import models
import jsonfield
from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mcq = jsonfield.JSONField(null=True, blank=True)
    saq = jsonfield.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

class Qplayer(models.Model):
    userProfile = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True)
    quizName = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=1, choices=[('N', "NotStarted"), ('S', "Started"), ('E', "Ended")], default='N')
    startTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
    score = models.IntegerField(null=True, default=0)
#   timeTaken = models.DurationField(null=True)

    def __str__(self):
        return self.userProfile.username + '_' + self.quizName

    def timeTaken(self):
        return self.endTime - self.startTime