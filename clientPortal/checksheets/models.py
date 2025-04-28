# checksheets/models.py
from django.db import models
import uuid

class Checksheet(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(default='', blank=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = f"https://example.com/client/{uuid.uuid4()}"
        super().save(*args, **kwargs)