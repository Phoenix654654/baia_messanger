from datetime import datetime

from django.db import models

from apps.abstract.custom_class import DateTimeWithoutTZField


class DeleteModel(models.Model):
    created_at = DateTimeWithoutTZField(auto_now_add=True)
    deleted_at = DateTimeWithoutTZField(null=True)
    modified_at = DateTimeWithoutTZField(auto_now=True)

    def delete(self, **kwargs):
        self.deleted_at = datetime.now()
        self.save()

    class Meta:
        abstract = True
