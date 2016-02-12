from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .utils import validate_version


class Category(models.Model):
    category=models.CharField(max_length=120, unique=True)
    image=models.ImageField(blank=True)

    class Meta:
        verbose_name_plural='categories'


    def __str__(self):
        return self.category


class Entry(models.Model):
    category=models.ForeignKey(Category)
    user=models.ForeignKey(User)
    name=models.CharField(max_length=120)
    description=models.TextField(max_length=1000)
    likes=models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural='entries'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('assets:detail', args=[self.id])

class EntryImage(models.Model):
    entry=models.ForeignKey(Entry)
    image=models.ImageField(blank=False)
    # is_primary=models.BooleanField()
    def __str__(self):
        return self.entry.name

class VersionHistory(models.Model):
    entry=models.ForeignKey(Entry)
    major_version = models.PositiveSmallIntegerField()
    minor_version = models.PositiveSmallIntegerField()
    patch_version = models.PositiveSmallIntegerField()
    timestamp=models.DateTimeField(auto_now=False, auto_now_add=True)
    file=models.FileField()
    changelog=models.TextField(max_length=1000)

    class Meta:
        verbose_name_plural='version history'

    def version(self):
        return str(self.major_version)+'.'+str(self.minor_version)+'.'+str(self.patch_version)

    def __str__(self):
        return self.entry
