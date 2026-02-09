from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import VotePoll 

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User 
        fields = ["username","password","email"]

class LoginIn(AuthenticationForm):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)

class VotingForm(forms.Form):
    candidate=forms.ModelChoiceField(
        queryset=VotePoll.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None,
    )
