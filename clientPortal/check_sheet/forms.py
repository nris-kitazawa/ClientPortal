# check_sheet/forms.py
from django import forms
from .models import CheckSheet

class CheckSheetForm(forms.ModelForm):
    class Meta:
        model = CheckSheet
        fields = ['title', 'description']  # ユーザーに入力してもらうフィールド

# check_sheet/forms.py
from django import forms
from .models import CheckSheetAnswer

class CheckSheetAnswerForm(forms.ModelForm):
    class Meta:
        model = CheckSheetAnswer
        fields = ['check_sheet', 'answer']  # 必要なフィールドを追加する

    # ここでフィールドにカスタムバリデーションを加えたり、ウィジェットをカスタマイズしたりできます。
