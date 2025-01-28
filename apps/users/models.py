from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.common.models import BaseModel, SECTION_CHOICES


ROLE_CHOICES = (
    ('ceo', 'CEO'),
    ('admin', 'Admin'),
)

class User(AbstractUser, BaseModel):
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, help_text="Role bo'lishi mumkin: 'ceo', 'admin'", default="admin")
    section = models.CharField(max_length=30, choices=SECTION_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "Foydalanuvchi "
        verbose_name_plural = "Foydalanuvchilar "