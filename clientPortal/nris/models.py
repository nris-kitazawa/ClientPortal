from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class NRIS(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='nris_users')
    user_permissions = models.ManyToManyField(Permission, related_name='nris_user_permissions')
