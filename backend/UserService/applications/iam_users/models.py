from django.db import models


class IAMUser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    user_id = models.CharField(max_length=255, unique=True)
    company_id = models.CharField(max_length=255, null=True, blank=True)
    is_authenticated = models.BooleanField(default=True)
    role_features = models.JSONField(default=list, blank=True)

    def __str__(self):
        return '{}-{}'.format(self.company_id, self.username)
