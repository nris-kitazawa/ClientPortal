# check_sheet/forms.py
from django import forms
from .models import *
from django.forms import modelformset_factory

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # フォームのラベルのサフィックスを空に設定
        kwargs.setdefault('label_suffix', '')
        # RadioSelectの初期値をNoneに設定
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.RadioSelect):
                self.fields[field_name].empty_label = None
                self.fields[field_name].initial = None
                field.choices = [(choice[0], choice[1]) for choice in field.choices if choice[0] != '']
        

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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.Textarea(attrs={
                'class': 'auto-resize-textarea',
                'rows': 1
            })

class LoginCredentialForm(BaseForm):
    class Meta:
        model = LoginCredential
        fields = '__all__'
        exclude = ['check_sheet']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.Textarea(attrs={
                'class': 'auto-resize-textarea',
                'rows': 1
            })

class CheckSheetDetailForm(BaseForm):
    class Meta:
        model = CheckSheet
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        for field in self.fields.values():
            field.disabled = True

class RequiredQuestionForm(BaseForm):
    class Meta:
        model = RequiredQuestion
        fields = '__all__'
        exclude = ['check_sheet']
        widgets = {
            'ip_address_management': forms.RadioSelect,
            'pre_application_status': forms.RadioSelect,
        }
