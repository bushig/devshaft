from django.db import models
from django.contrib.auth.models import User

from common.models import License


class Framework(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=1000)
    license = models.ForeignKey(License, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'frameworks'

    def __str__(self):
        return self.name
