# check_sheet/models.py
from django.db import models
from django.contrib.auth.models import User
import random
import string
import uuid

class CheckSheet(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)  # チェックシートのタイトル
    description = models.TextField(null=True, blank=True)  # チェックシートの説明
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # 作成者（NRISユーザー）
    password = models.CharField(max_length=10, null=True, blank=True)  # クライアント用のパスワード
    id = models.CharField(primary_key=True, max_length=100)

    #Contents
    system_name = models.CharField(max_length=100, null=True, blank=True)
    purpose = models.TextField(null=True, blank=True)
    environment = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    release_status = models.CharField(max_length=50, null=True, blank=True)
    url_or_ip = models.CharField(max_length=100, null=True, blank=True)
    host_name = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    web_server = models.CharField(max_length=100, null=True, blank=True)
    app_server = models.CharField(max_length=100, null=True, blank=True)
    framework = models.CharField(max_length=100, null=True, blank=True)
    db_server = models.CharField(max_length=100, null=True, blank=True)
    login_id = models.CharField(max_length=100, null=True, blank=True)
    login_password = models.CharField(max_length=100, null=True, blank=True)
    permission = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
    outsourcing_info = models.TextField(null=True, blank=True)
    aws_services = models.TextField(null=True, blank=True)
    session_timeout = models.IntegerField(null=True, blank=True)
    password_encryption = models.CharField(max_length=100, null=True, blank=True)
    password_expiry = models.IntegerField(null=True, blank=True)
    password_reuse_limit = models.IntegerField(null=True, blank=True)
    initial_password_change = models.BooleanField(null=True, blank=True)
    supported_browsers = models.TextField(null=True, blank=True)
    credit_card_info = models.TextField(null=True, blank=True)
    waf_info = models.TextField(null=True, blank=True)
    cms_info = models.TextField(null=True, blank=True)
    file_upload_info = models.TextField(null=True, blank=True)
    shell_info = models.TextField(null=True, blank=True)
    c_library_info = models.TextField(null=True, blank=True)
    log4j_info = models.TextField(null=True, blank=True)
    spring_info = models.TextField(null=True, blank=True)
    security_measures = models.TextField(null=True, blank=True)
    diagnostic_date = models.DateField(null=True, blank=True)
    diagnostic_time = models.TimeField(null=True, blank=True)
    extension_possible = models.BooleanField(null=True, blank=True)
    extension_contact = models.CharField(max_length=100, null=True, blank=True)
    report_recipient = models.CharField(max_length=100, null=True, blank=True)
    onsite_contact = models.CharField(max_length=100, null=True, blank=True)
    server_info = models.TextField(null=True, blank=True)
    diagnostic_ip_info = models.TextField(null=True, blank=True)
    diagnostic_notes = models.TextField(null=True, blank=True)



    def save(self, *args, **kwargs):
        if not self.password:
            self.password = self.generate_password()
        if not self.id:
            self.id = self.generate_custom_uuid()
            self.id.editable=False
        super(CheckSheet, self).save(*args, **kwargs)

    def generate_custom_uuid(self): 
        return f"{uuid.uuid4()}-{uuid.uuid4()}"

    def generate_password(self):
        """パスワードをランダムに生成"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def getURL(self):
        """URLをランダムに生成"""
        return f"/check_sheet/{self.id}/"

    def __str__(self):
        return self.title


