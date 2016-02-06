from django.db import models

class Category(models.Model):
    category=models.CharField(max_length=120, unique=True)
    image=models.ImageField(blank=True)

    def __str__(self):
        return self.category


class Entry(models.Model):
    category=models.ForeignKey(Category)
    name=models.CharField(max_length=120)
    description=models.TextField(max_length=1000)
    likes=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class EntryImages(models.Model):
    entry=models.ForeignKey(Entry)
    image=models.ImageField()

class VersionHistory(models.Model):
    entry=models.ForeignKey(Entry)
    version=models.CharField(max_length=6)
    timestamp=models.DateTimeField(auto_now=False, auto_now_add=True)
    file=models.FileField()
    changelog=models.TextField(max_length=1000)

    def __str__(self):
        return self.version
