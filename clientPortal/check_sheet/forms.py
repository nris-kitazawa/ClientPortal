# check_sheet/forms.py
from django import forms
from .models import *

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

from django.forms import modelformset_factory
AssessTargetFormSet = modelformset_factory(
    AssessTarget,
    form=AssessTargetForm,
    extra=1,  # 新規追加用の空フォーム数
    can_delete=True  # 行の削除も可能に
)

class CheckSheetDetailForm(BaseForm):
    class Meta:
        model = CheckSheet
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        for field in self.fields.values():
            field.disabled = True
