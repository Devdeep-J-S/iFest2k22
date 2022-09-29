from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime, AdminTimeWidget
from .models import *
from django.forms import DateTimeInput

class CreateUserForm(UserCreationForm):
    #DOB = forms.DateField(
    #    label='Date of Birth',
    #    help_text='Required.',
    #    widget=forms.SelectDateWidget(years=range(1998, 2010))
    #)
    email = forms.EmailField(label='Email', help_text='Required.', required=True)
    first_name = forms.CharField(label='First Name', max_length=150, help_text='Required.')
    last_name = forms.CharField(label='Last Name', max_length=150, required=False)
    university = forms.CharField(label='University', help_text='Required.')
    contact_number = forms.CharField(label='Contact Number', help_text='Required.') 
    ieee_id = forms.CharField(label='IEEE ID', max_length=10, required=False)
    referral_code = forms.CharField(label='Referral Code', max_length=12, required=False)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "university", "contact_number", "ieee_id", "referral_code", "password1", "password2"]


class UpdateUserForm(forms.ModelForm):
    #DOB = forms.DateField(
    #    help_text='Required.',
    #    widget=forms.SelectDateWidget(years=range(1998, 2010))
    #)
    university = forms.CharField(help_text='Required.')
    contact_number = forms.CharField(
        help_text='Required.',
        validators=[MinValueValidator('1000000000'), MaxValueValidator('9999999999')]
    )

    class Meta:
        model = User
        fields = ["first_name", "university","contact_number"]
