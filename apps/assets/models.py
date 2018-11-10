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

from .utils import version_filename_save
from apps.common.models import License
from apps.common.repos import get_repo_for_repo_url
from apps.languages.models import Language
from apps.frameworks.models import Framework


class AssetManager(models.Manager):
    def get_queryset(self):
        return super(AssetManager, self).get_queryset().select_related('category', 'user', 'license').annotate(
            Count('users_liked', distinct=True))

    def with_image(self):
        return self.get_queryset().prefetch_related('images')

    def not_null(self):
        return self.get_queryset().exclude(releases__isnull=True)


class Category(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    image = models.ImageField(blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Asset(models.Model):
    # TYPES = (
    #     (0, 'Releases'),
    #     (1, 'Commits'),
    #     (2, 'Github Releases')
    # )
    category = TreeForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    languages = models.ManyToManyField(Language, related_name="assets", blank=True)
    frameworks = models.ManyToManyField(Framework, related_name="assets", blank=True)
    license = models.ForeignKey(License, on_delete=models.PROTECT)
    name = models.CharField(max_length=40)
    users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='entry_liked', blank=True)
    description = models.TextField(max_length=5000)
    repository = models.URLField(blank=True, null=True, max_length=300)
    site = models.URLField(blank=True, null=True, max_length=300)

    repo_stars = models.IntegerField("Stars", blank=True, null=True)
    repo_forks = models.IntegerField("Repo forks", blank=True, null=True)
    repo_description = models.CharField("Repo description", null=True, max_length=1000, blank=True)
    repo_updated = models.DateTimeField(null=True, blank=True)
    last_commit = models.DateTimeField(null=True, blank=True)
    commits = models.CharField(null=True, blank=True, max_length=500,
                               validators=[validate_comma_separated_integer_list])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)

    # Settings
    # update_type = models.IntegerField(default=0, choices=TYPES)

    # managers
    objects = AssetManager()

    def liked(self, user):
        return Asset.objects.filter(id=self.id, users_liked=user).exists()

    @property
    def total_likes(self):
        return Asset.objects.get(id=self.id).users_liked.count()

    @property
    def repo(self):
        return get_repo_for_repo_url(self.repository)

    def repo_name(self):
        return re.sub(self.repo.url_regex, '', self.repository)

    def fetch_metadata(self):
        self.repo.fetch_metadata(self)
        self.save()

    class Meta:
        ordering = ['-updated']
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('assets:detail', args=[self.id])


class AssetImage(models.Model):
    entry = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='images')
    image = ImageCropField(blank=True, upload_to='uploaded_images')
    cropping = ImageRatioField('image', '300x300')
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.entry.name

    class Meta:
        ordering = ['date_add']


class Release(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='releases')
    version = models.CharField(max_length=25)
    timestamp = models.DateTimeField('Date of this release', default=timezone.now)
    changelog = models.TextField(max_length=10000, blank=True)

    class Meta:
        verbose_name_plural = 'version history'
        ordering = ("-timestamp",)
        get_latest_by = "timestamp"

    def __str__(self):
        return self.version


class ReleaseUpload(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE, related_name='uploads')
    note = models.CharField('Note on file', max_length=15)
    file = models.FileField(upload_to=version_filename_save, blank=True)
