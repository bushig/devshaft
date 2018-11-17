from django.db import models

from zinnia.models_bases.entry import AbstractEntry
from apps.frameworks.models import Framework
from apps.assets.models import Asset
from apps.tutorials.models import Series


class NewsEntry(AbstractEntry):
    frameworks = models.ManyToManyField(Framework, related_name='news', blank=True)
    assets = models.ManyToManyField(Asset, related_name='news', blank=True)
    series = models.ManyToManyField(Series, related_name='news', blank=True)

    class Meta(AbstractEntry.Meta):
        abstract = True
