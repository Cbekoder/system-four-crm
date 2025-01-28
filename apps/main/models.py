from django.db import models
from apps.common.models import BaseModel, SECTION_CHOICES
from apps.users.models import User


class Expense(BaseModel):
    reason = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.CharField(max_length=30, choices=SECTION_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.reason