import json
from django.db import models
import jsonfield
from django.contrib.auth.models import User

# Create your models here.

class Puzzle(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    link = models.CharField(max_length=256, null=True, unique=True)
    Data = jsonfield.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    userProfile = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=[('N', "NotStarted"), ('S', "Started"), ('E', "Ended")], default='N')
    startTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
#    timeTaken = models.DurationField(null=True)

    def __str__(self):
        return self.userProfile.username + '_' + 'IOH'

    def timeTaken(self):
        return self.endTime - self.startTime