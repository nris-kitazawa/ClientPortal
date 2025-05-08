# check_sheet/models.py
from django.db import models
from django.contrib.auth.models import User
import random
import string
import uuid

class CheckSheet(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='タイトル')  # チェックシートのタイトル
    guest_comapny_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='お客様社名')  # ゲスト会社名
    answered_by = models.CharField(max_length=200, null=True, blank=True, verbose_name='記入者')  # ゲスト
    answered_at = models.DateField(null=True, blank=True, verbose_name='記入日')  # 回答日

    id = models.CharField(primary_key=True, max_length=100, editable=False)
    password = models.CharField(max_length=64, null=True, blank=True)  

    created_by = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="created_check_sheets")  # 作成者（NRISユーザー）
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = self.generate_password()
        if not self.id:
            self.id = self.generate_custom_uuid()
        super(CheckSheet, self).save(*args, **kwargs)

    def generate_custom_uuid(self): 
        return f"{uuid.uuid4()}-{uuid.uuid4()}"

    def generate_password(self):
        """パスワードをランダムに生成"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def __str__(self):
        return self.title
    
class SystemSummary(models.Model):
    ENV_CHOICES = [
        ('production', '本番環境'),
        ('development', '開発環境'),
        ('maintenance', '保守環境'),
        ('other', 'その他'),
    ]

    check_sheet = models.ForeignKey(CheckSheet, on_delete=models.CASCADE)  # CheckSheetのidを外部キーとして登録
    system_name = models.CharField(max_length=200, verbose_name='システム正式名称', null=True)
    system_abbr_name = models.CharField(max_length=200, verbose_name='システム略称', null=True)
    system_overview = models.TextField(verbose_name='システムの利用目的', null=True)
    environment = models.CharField(
        max_length=20,
        choices=ENV_CHOICES,
        verbose_name='診断実施環境',
        null=True,
        blank=True,
    )
    environment_other = models.CharField(
        max_length=200,
        verbose_name='',
        null=True,
        blank=True,
    )
    dev_lang = models.TextField(verbose_name='開発言語', null=True)
    is_released = models.BooleanField(default=False, verbose_name='リリース済', null=True)
    release_date = models.DateField(verbose_name='リリース日', null=True)

    def __str__(self):
        return self.system_name

# check_sheet/models.py

class AssessTarget(models.Model):
    check_sheet = models.ForeignKey(CheckSheet, on_delete=models.CASCADE, related_name='assess_targets')
    url_or_ip_address = models.CharField(max_length=200, verbose_name='診断対象のURLまたはIPアドレス', null=True)
    host_name = models.CharField(max_length=200, verbose_name='ホスト名', null=True)
    os = models.CharField(max_length=200, verbose_name='OS', null=True)
    web_server = models.CharField(max_length=200, verbose_name='Webサーバ', null=True)
    ap_server = models.CharField(max_length=200, verbose_name='APサーバ', null=True)
    framework = models.CharField(max_length=200, verbose_name='フレームワーク', null=True)
    db_server = models.CharField(max_length=200, verbose_name='DBサーバ', null=True)

class LoginCredential(models.Model):
    check_sheet = models.ForeignKey(
        'CheckSheet', 
        on_delete=models.CASCADE, 
        related_name='login_credentials'
    )
    login_id = models.CharField(max_length=255, verbose_name="ログインID")
    password = models.CharField(max_length=255, verbose_name="パスワード")
    role = models.CharField(max_length=255, verbose_name="権限")