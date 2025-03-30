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
    ("factory", "Zavod")
)

CURRENCY_TYPE = (
    ("USD", "USD🇺🇸"),
    ("UZS", "UZS🇺🇿"),
    ("RUB", "RUB🇷🇺")
)

class User(AbstractUser):
    balance = models.FloatField(default=0, verbose_name="Qoldiq")
    currency_type = models.CharField(max_length=10, choices=CURRENCY_TYPE, default="USD")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, help_text="Role bo'lishi mumkin: 'ceo', 'admin'", default="admin")
    section = models.CharField(max_length=30, choices=SECTION_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "Foydalanuvchi "
        verbose_name_plural = "Foydalanuvchilar "

    def __str__(self):
        return self.get_full_name() if self.get_full_name() else self.username


