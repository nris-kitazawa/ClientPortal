# check_sheet/forms.py
from django import forms
from .models import *
from django.forms import modelformset_factory

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # フォームのラベルのサフィックスを空に設定
        self.label_suffix = ''  # 修正ポイント
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

from django import forms
from .models import RequiredQuestion

class RequiredQuestionForm(BaseForm):
    pre_application_required = forms.TypedChoiceField(
        label='事前申請が必要ですか',
        choices=[(True, 'はい'), (False, 'いいえ')],
        coerce=lambda x: x == 'True',  # 'True' を Python の True に変換
        widget=forms.RadioSelect,
        required=False  # 必須にする場合は True に変更
    )

    class Meta:
        model = RequiredQuestion
        fields = '__all__'
        exclude = ['check_sheet']
        widgets = {
            'ip_address_management': forms.RadioSelect,
            'pre_application_status': forms.RadioSelect,
        }

    def clean_outsourcing_info(self):
        """
        外部委託先の情報が必要な場合にバリデーションを行う
        """
        ip_address_management = self.cleaned_data.get('ip_address_management')
        outsourcing_info = self.cleaned_data.get('outsourcing_info')

        if ip_address_management != '自社管理' and not outsourcing_info:
            raise forms.ValidationError('外部委託先の情報を入力してください。')

        return outsourcing_info

    def clean_pre_application_status(self):
        """
        事前申請が必要な場合に申請状況をチェック
        """
        pre_application_required = self.cleaned_data.get('pre_application_required')
        pre_application_status = self.cleaned_data.get('pre_application_status')

        if pre_application_required and not pre_application_status:
            raise forms.ValidationError('申請状況を選択してください。')

        return pre_application_status

    def clean(self):
        """
        全体のバリデーションを実行
        """
        cleaned_data = super().clean()
        # 他のフィールドのバリデーションを呼び出す
        self.clean_outsourcing_info()
        self.clean_pre_application_status()

        return cleaned_data
    
class PreparedDocsForm(BaseForm):

    class Meta:
        model = PreparedDocs
        fields = '__all__'
        exclude = ['check_sheet']
        widgets = {
            'session_management_design': forms.CheckboxInput(),
            'authentication_design': forms.CheckboxInput(),
            'target_screen_list': forms.CheckboxInput(),
            'screen_transition_diagram': forms.CheckboxInput(),
            'network_configuration_diagram': forms.CheckboxInput(),
            'web_server_directory_list': forms.CheckboxInput(),
        }


class AssessScheduleForm(BaseForm):

    def create_typed_choice_field(label, choices):
        return forms.TypedChoiceField(
            choices=choices,
            coerce=lambda x: x == 'True',
            widget=forms.RadioSelect,
            required=False,
            label=label
        )

    extension_possible = create_typed_choice_field('延長可否', [(True, '必要'), (False, '不要')])
    extension_contact = create_typed_choice_field('連絡要否', [(True, '必要'), (False, '不要')])
    extension_continue = create_typed_choice_field('連絡不通時の続行', [(True, '可能'), (False, '不可能')])

    class Meta:
        model = AssessSchedule
        fields = '__all__'  # すべてのフィールドをフォームに含める
        exclude = ['check_sheet']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'value': '07:00'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'value': '22:00'}),
            'backup_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        extension_contact = cleaned_data.get('extension_contact')
        extension_continue = cleaned_data.get('extension_continue')

        if extension_contact and not extension_continue:
            raise forms.ValidationError('連絡は必要としてください。')

        return cleaned_data

class MemberForm(BaseForm):
    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['check_sheet']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.Textarea(attrs={
                'class': 'auto-resize-textarea',
                'rows': 1
            })