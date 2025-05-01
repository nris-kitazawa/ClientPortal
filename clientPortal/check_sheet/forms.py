# check_sheet/forms.py
from django import forms
from .models import CheckSheet

class CheckSheetForm(forms.ModelForm):
    class Meta:
        model = CheckSheet
        fields = ['title', 'description']  # ユーザーに入力してもらうフィールド

class CheckSheetEditForm(forms.ModelForm):
    class Meta:
        model = CheckSheet
        fields = '__all__'

class CheckSheetDetailForm(forms.ModelForm):
    class Meta:
        model = CheckSheet
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        for field in self.fields.values():
            field.disabled = True
