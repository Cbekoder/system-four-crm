from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
    ('ceo', 'CEO'),
    ('admin', 'Admin'),
)

SECTION_CHOICES = (
    ("logistic", "Logistika"),
    ("fridge", "Muzlatgich"),
    ("garden", "Bog'"),
    ("factory", "Zavod"),
    ("general", "Umumiy")
)

class User(AbstractUser):
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, help_text="Role bo'lishi mumkin: 'ceo', 'admin'", default="admin")
    section = models.CharField(max_length=30, choices=SECTION_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "Foydalanuvchi "
        verbose_name_plural = "Foydalanuvchilar "


