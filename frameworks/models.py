from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import validate_comma_separated_integer_list
from django.utils import timezone

import re

from image_cropping import ImageRatioField, ImageCropField

from common.repos import get_repo_for_repo_url
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

# class Orientation(models.Model):
    # title = models.CharField(max_length=2)

class Platform(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Framework(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=1000)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    is_2d = models.BooleanField()
    is_3d = models.BooleanField()
    languages = models.ManyToManyField(Language)
    target_platforms = models.ManyToManyField(Platform, related_name='target_platforms')
    editor_platforms = models.ManyToManyField(Platform, related_name='editor_platforms')
    site = models.URLField(blank=True)
    repository_url = models.URLField(blank=True) #if not null then its open source
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=False, default=timezone.now)

    repo_stars = models.IntegerField("Stars", default=0)
    repo_forks = models.IntegerField("Repo forks", default=0)
    repo_description = models.CharField("Repo description", null=True, max_length=1000)
    repo_updated = models.DateTimeField(null=True)
    commits = models.CharField(null=True, blank=True, max_length=500,
                               validators=[validate_comma_separated_integer_list])

    # images
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='frameworks_liked', blank=True)

    class Meta:
        verbose_name_plural = 'frameworks'

    #cache with signals
    def liked(self, user):
        return self.objects.filter(pk=self.pk, likes=user).exists()

    @property
    def total_likes(self):
        return Framework.objects.get(id=self.id).likes.count()

    @property
    def repo(self):
        return get_repo_for_repo_url(self.repository_url)

    def repo_name(self):
        return re.sub(self.repo.url_regex, '', self.repository_url)

    def fetch_metadata(self):
        self.repo.fetch_metadata(self)
        self.save()


    def is_author(self, user):
        return self.user == user

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('frameworks:detail', kwargs={'pk': self.pk})

class FrameworkImage(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    image=ImageCropField(blank=True, upload_to='uploaded_images')
    cropping = ImageRatioField('image', '300x300')