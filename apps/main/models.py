from django.db import models
from apps.common.models import BaseModel
from apps.users.models import User


class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Expense(BaseModel):
    reason = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.reason