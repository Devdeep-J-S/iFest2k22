from unittest.util import _MAX_LENGTH
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.utils import timezone
import os
import jsonfield


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    university = models.CharField(max_length=50, null=True)
    #DOB = models.DateField(null=True)
    payment = models.BooleanField(null=True)
    contact_number = models.CharField(max_length=12, null=True)
    order_id = models.CharField(max_length=100,null=True,blank=True)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    ieee_id = models.CharField(max_length=10, null=True, blank=True)
    referral_code = models.CharField(max_length=12, null=True, blank=True)
    staffAuth = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class campusAmbassador(models.Model):
    referral_code = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    rounds = models.PositiveIntegerField(null=True)
    paid = models.BooleanField(null=True)
    registrationDeadline = models.DateTimeField(null=True)
    logo = models.ImageField(default="profile.png", null=True, blank=True)
    Data = jsonfield.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Registration(models.Model):
    userProfile = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        if self.userProfile and self.event:
            return self.userProfile.username + " " + self.event.name
