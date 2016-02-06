from django.db import models

class Categoty(models.Model):
    categoty=models.CharField(max_length=120, unique=True)


class Entry(models.Model):
    category=models.ForeignKey(Categoty)
    name=models.CharField(max_length=120)
    description=models.TextField(max_length=1000)



class VersionHistory(models.Model):
    entry=models.ForeignKey(Entry)
    version=models.CharField(max_length=6)
    timestamp=models.DateTimeField(auto_now=False, auto_now_add=True)
    changelog=models.TextField(max_length=1000)
