import re

from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.core.validators import validate_comma_separated_integer_list
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey
from image_cropping import ImageRatioField, ImageCropField
from markdownx.models import MarkdownxField
import tagulous.models

from apps.common.models import License
from apps.common.repos import get_repo_for_repo_url
from apps.languages.models import Language
from apps.frameworks.models import Framework
from apps.assets.models import Asset


class TutorialManager(models.Manager):
    def get_queryset(self):
        return super(TutorialManager, self).get_queryset().annotate(total_likes=Count('users_liked', distinct=True))


class SeriesManager(models.Manager):
    def get_queryset(self):
        return super(SeriesManager, self).get_queryset().annotate(total_likes=Count('users_liked', distinct=True))


class Tutorial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    languages = models.ManyToManyField(Language, related_name="tutorials", blank=True)
    frameworks = models.ManyToManyField(Framework, related_name="tutorials", blank=True)
    assets = models.ManyToManyField(Asset, related_name='tutorials', blank=True)
    tags = tagulous.models.TagField(
        force_lowercase=True,
        space_delimiter=False,
        tree=True
    )
    users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tutorials_liked', blank=True)

    name = models.CharField(max_length=60)
    short_description = models.CharField(max_length=500, blank=True)
    content = MarkdownxField(blank=True)
    url = models.URLField(blank=True, null=True, max_length=300)
    credit_note = models.CharField(max_length=255, blank=True)

    image = ImageCropField(blank=True, upload_to='uploaded_images')
    cropping = ImageRatioField('image', '300x300')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    # image field with asset image that displayed on on lists. if no image, then it will be equal to first uploaded
    # image in AssetImage for that asset

    # Settings

    objects = TutorialManager()

    def liked(self, user):
        return Tutorial.objects.filter(id=self.id, users_liked=user).exists()

    class Meta:
        ordering = ['-updated']
        verbose_name_plural = 'tutorials'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tutorials:detail', args=[self.id])


class TutorialImage(models.Model):
    tutorial = models.ForeignKey(Framework, on_delete=models.CASCADE)
    image = ImageCropField(blank=True, upload_to='uploaded_images')
    cropping = ImageRatioField('image', '300x300')
    date_add = models.DateTimeField(auto_now_add=True)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['order', 'date_add']


class Series(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    languages = models.ManyToManyField(Language, related_name="series", blank=True)
    frameworks = models.ManyToManyField(Framework, related_name="series", blank=True)
    assets = models.ManyToManyField(Asset, related_name='series', blank=True)
    users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='series_liked', blank=True)
    tags = tagulous.models.TagField(to=Tutorial.tags.tag_model)

    tutorials = models.ManyToManyField(Tutorial, through='TutorialMembership')

    name = models.CharField(max_length=40)
    short_description = models.CharField(max_length=500, blank=True)
    content = MarkdownxField(blank=True)
    credit_note = models.CharField(max_length=255, blank=True)

    image = ImageCropField(blank=True, upload_to='uploaded_images')
    cropping = ImageRatioField('image', '300x300')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)

    objects = TutorialManager()

    def liked(self, user):
        return Series.objects.filter(id=self.id, users_liked=user).exists()

    class Meta:
        ordering = ['-updated']
        verbose_name_plural = 'series'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tutorials:series_detail', args=[self.id])


class TutorialMembership(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        unique_together = ("tutorial", "series")
