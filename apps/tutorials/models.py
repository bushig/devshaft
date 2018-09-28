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

    name = models.CharField(max_length=40)
    users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tutorials_liked', blank=True)
    description = MarkdownxField()
    url = models.URLField(blank=True, null=True, max_length=300)
    youtube = models.URLField(blank=True, null=True, max_length=300)
    credit_note = models.CharField(max_length=255, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    #image field with asset image that displayed on on lists. if no image, then it will be equal to first uploaded
    #image in AssetImage for that asset

    # Settings
    locked = models.BooleanField('Editing is closed', default=True)

    def liked(self, user):
        return Asset.objects.filter(id=self.id, users_liked=user).exists()

    @property
    def total_likes(self):
        return self.users_liked.count()

    class Meta:
        ordering = ['-updated']
        verbose_name_plural='tutorials'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tutorials:detail', args=[self.id])
