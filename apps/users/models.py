from django.contrib.auth.models import AbstractUser

from apps.common.models import BaseModel


# Create your models here.
class User(AbstractUser, BaseModel):

    class Meta:
        verbose_name = "Foydalanuvchi "
        verbose_name_plural = "Foydalanuvchilar "