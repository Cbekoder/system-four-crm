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


class VersionHistory(BaseModel):
    version = models.CharField(max_length=64)
    required = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Version history"
        verbose_name_plural = "Version histories"

    def __str__(self):
        return self.version