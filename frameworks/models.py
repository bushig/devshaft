from django.db import models
from django.contrib.auth.models import User

from common.models import License
from languages.models import Language

PLATFORMS_CHOISES = ((1, 'Windows'),
                     (2, 'Linux'),
                     (3, 'Mac'),
                     (4, 'Android'),
                     (5, 'iOS'),
                     (6, 'Web'))

ORIENTATION_CHOICES = ((1, '2D&3D'),
                       (2, '2D'),
                       (3, '3D'))


class Platform(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Framework(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=1000)
    license = models.ForeignKey(License, blank=True, null=True)
    orientation = models.IntegerField(choices=ORIENTATION_CHOICES, default=1)
    languages = models.ManyToManyField(Language)
    target_platforms = models.ManyToManyField(Platform, related_name='target_platforms')
    editor_platforms = models.ManyToManyField(Platform, related_name='editor_platforms')
    # images
    # likes

    class Meta:
        verbose_name_plural = 'frameworks'

    def __str__(self):
        return self.title
