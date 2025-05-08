# check_sheet/forms.py
from django import forms
from .models import *
from django.forms import modelformset_factory

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

class CheckSheetForm(BaseForm):
    class Meta:
        model = CheckSheet
        fields = ['title']  # ユーザーに入力してもらうフィールド

class CheckSheetEditForm(BaseForm):
    class Meta:
        model = CheckSheet
        fields = '__all__'
        exclude = ['created_by', 'password', 'id']
        widgets = {
            "answered_at": forms.widgets.NumberInput(attrs={
                "type": "date"
            })
        }

class SystemSummaryForm(BaseForm):
    class Meta:
        model = SystemSummary
        fields = '__all__'
        exclude = ['check_sheet']
        widgets = {
            'environment': forms.RadioSelect,
            'environment_other': forms.TextInput(attrs={'id': 'env_other_field'}),
            "release_date": forms.widgets.NumberInput(attrs={
                "type": "date"
            })
        }

class AssessTargetForm(BaseForm):
    class Meta:
        model = AssessTarget
        fields = '__all__'
        exclude = ['check_sheet']

class LoginCredentialForm(BaseForm):
    class Meta:
        model = LoginCredential
        fields = '__all__'
        exclude = ['check_sheet']

class CheckSheetDetailForm(BaseForm):
    class Meta:
        model = CheckSheet
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        for field in self.fields.values():
            field.disabled = True
