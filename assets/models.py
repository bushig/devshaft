from django.db import models
from django.contrib.auth.models import User


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

class EntryImage(models.Model):
    entry=models.ForeignKey(Entry)
    image=models.ImageField()
    # is_primary=models.BooleanField()

class VersionHistory(models.Model):
    entry=models.ForeignKey(Entry)
    version=models.CharField(max_length=6)
    timestamp=models.DateTimeField(auto_now=False, auto_now_add=True)
    file=models.FileField()
    changelog=models.TextField(max_length=1000)

    class Meta:
        verbose_name_plural='version history'


    def __str__(self):
        return self.version
