# check_sheet/models.py
from django.db import models
from django.contrib.auth.models import User
import random
import string

class CheckSheet(models.Model):
    title = models.CharField(max_length=200)  # チェックシートのタイトル
    description = models.TextField()  # チェックシートの説明
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # 作成者（NRISユーザー）
    password = models.CharField(max_length=10)  # クライアント用のパスワード
    url = models.URLField(blank=True)  # クライアントに送信するURL

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = self.generate_password()
        if not self.url:
            self.url = self.generate_url()
        super(CheckSheet, self).save(*args, **kwargs)

    def generate_password(self):
        """パスワードをランダムに生成"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def generate_url(self):
        """URLをランダムに生成"""
        return f"/check_sheet/{self.pk}/{self.password}/"

    def __str__(self):
        return self.title
    
# check_sheet/models.py
from django.db import models
from django.contrib.auth.models import User
from .models import CheckSheet

class CheckSheetAnswer(models.Model):
    check_sheet = models.ForeignKey(CheckSheet, on_delete=models.CASCADE)  # チェックシート
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ゲストユーザー
    answer = models.TextField()  # 回答内容

    def __str__(self):
        return f"Answer for {self.check_sheet.title} by {self.user.username}"

