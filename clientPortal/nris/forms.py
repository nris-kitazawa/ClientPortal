from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import NRIS

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = NRIS
        fields = ('username', 'password1', 'password2')
