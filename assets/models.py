import re

from django.db import models
from django.db.models import Count, F, Max
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import validate_comma_separated_integer_list
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey
from image_cropping import ImageRatioField, ImageCropField

from .utils import version_filename_save
from common.models import License
from .repos import get_repo_for_repo_url
from languages.models import Language
from frameworks.models import Framework

class EntryManager(models.Manager):
    def get_queryset(self):
        return super(EntryManager, self).get_queryset().select_related('category', 'user').prefetch_related('entryimage_set').\
            defer('user__password').annotate(Count('users_liked', distinct=True))

    def not_null(self):
        return self.get_queryset().exclude(versionhistory__isnull=True)


class Category(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    image = models.ImageField(blank=True)

    class Meta:
        verbose_name_plural='categories'


    def __str__(self):
        return self.name


class Entry(models.Model): #make it assets again!
    category=TreeForeignKey(Category, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=40)
    description=models.TextField(max_length=5000)
    license = models.ForeignKey(License, on_delete=models.PROTECT)
    repository = models.URLField(blank=True, null=True, max_length=100)
    site = models.URLField(blank=True, null=True, max_length=100)
    users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='entry_liked')
    languages = models.ManyToManyField(Language, related_name="assets")
    frameworks = models.ManyToManyField(Framework, related_name="assets", blank=True)

    repo_stars = models.IntegerField("Stars", default=0)
    repo_forks = models.IntegerField("Repo forks", default=0)
    repo_description = models.CharField("Repo description", null=True, max_length=1000)
    repo_updated = models.DateTimeField(null=True)
    commits = models.CharField(null=True, blank=True, max_length=500, validators=[validate_comma_separated_integer_list])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    #image field with asset image that displayed on on lists. if no image, then it will be equal to first uploaded
    #image in EntryImage for that asset

    # Settings
    choices = ((0, 'Github'),
               (1, 'Versions'),
               (2, 'Link')
               )
    entry_type = models.PositiveSmallIntegerField(choices=choices)
    github_releases = models.BooleanField(default=False)
    changelog = models.BooleanField(default=False)
    locked = models.BooleanField(default=True)


    #managers
    objects = EntryManager()

    def liked(self, user):
        return Entry.objects.filter(id=self.id, users_liked=user).exists()

    @property
    def total_likes(self):
        return Entry.objects.get(id=self.id).users_liked.count()

    @property
    def repo(self):
        return get_repo_for_repo_url(self.repository)

    def repo_name(self):
        return re.sub(self.repo.url_regex, '', self.repository)

    def fetch_metadata(self):
        self.repo.fetch_metadata(self)
        self.save()

    class Meta:
        verbose_name_plural='entries'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('assets:detail', args=[self.id])

class EntryImage(models.Model):
    entry=models.ForeignKey(Entry, on_delete=models.CASCADE)
    image=ImageCropField(blank=True, upload_to='uploaded_images')
    cropping = ImageRatioField('image', '300x300')

    def __str__(self):
        return self.entry.name


class VersionHistory(models.Model):
    entry=models.ForeignKey(Entry, on_delete=models.CASCADE)
    version = models.CharField(max_length=25)
    is_github_release = models.BooleanField(default=False)
    release_id = models.IntegerField("Github release ID", db_index=True, null=True, blank=True)
    download_url = models.URLField(null=True, blank=True)
    timestamp=models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)
    file=models.FileField(upload_to=version_filename_save, blank=True) # TODO: upload to VERSIONS
    changelog=models.TextField(max_length=1000, blank=True)

    class Meta:
        verbose_name_plural='version history'
        ordering = ("-timestamp",)
        get_latest_by = "timestamp"

    def __str__(self):
        return self.version
