# checksheets/forms.py
from django import forms
from .models import Checksheet

class ChecksheetForm(forms.ModelForm):
    class Meta:
        model = Checksheet
        fields = ['title', 'password']
