from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # add updated_at field to update_fields if it is not present
        # so that updated_at field will always be updated
        if update_fields and "updated_at" not in update_fields:
            update_fields.append("updated_at")

        super().save(force_insert, force_update, using, update_fields)


CURRENCY_TYPE = (
    ("USD", "USD🇺🇸"),
    ("UZS", "UZS🇺🇿")
)


class BasePerson(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    extra_phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    balance = models.FloatField(default=0)
    debt = models.FloatField(default=0)
    landing = models.FloatField(default=0)
    balance_type = models.CharField(max_length=10, choices=CURRENCY_TYPE, default="UZS")

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if update_fields and "updated_at" not in update_fields:
            update_fields.append("updated_at")

        super().save(force_insert, force_update, using, update_fields)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class VersionHistory(BaseModel):
    version = models.CharField(max_length=64)
    required = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Version history"
        verbose_name_plural = "Version histories"

    def __str__(self):
        return self.version