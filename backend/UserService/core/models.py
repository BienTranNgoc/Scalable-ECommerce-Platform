from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ExcludeDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)
