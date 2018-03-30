from django.db import models
from django.db.models import Count, F, Max
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError

from .utils import version_filename_save


class EntryManager(models.Manager):
    def get_queryset(self):
        return super(EntryManager, self).get_queryset().select_related('category', 'user').prefetch_related('entryimage_set').\
            defer('user__password').annotate(Max('versionhistory__timestamp', distinct=True), Count('users_liked', distinct=True))

    def not_null(self):
        return self.get_queryset().exclude(versionhistory__isnull=True)


class Category(models.Model):
    category=models.CharField(max_length=120, unique=True)
    image=models.ImageField(blank=True)

    class Meta:
        verbose_name_plural='categories'


    def __str__(self):
        return self.category


class Entry(models.Model): #make it assets again!
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=40)
    description=models.TextField(max_length=1000)
    users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='entry_liked')
    #image field with asset image that displayed on on lists. if no image, then it will be equal to first uploaded
    #image in EntryImage for that asset

    #managers
    objects = EntryManager()

    def liked(self, user):
        return Entry.objects.filter(id=self.id, users_liked=user).exists()

    @property
    def total_likes(self):
        return Entry.objects.first(id=self.id).users_liked.count()

    class Meta:
        verbose_name_plural='entries'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('assets:detail', args=[self.id])

class EntryImage(models.Model):
    entry=models.ForeignKey(Entry, on_delete=models.CASCADE)
    image=models.ImageField(blank=False)

    def __str__(self):
        return self.entry.name


class VersionHistory(models.Model):
    entry=models.ForeignKey(Entry, on_delete=models.CASCADE)
    major_version = models.PositiveSmallIntegerField()
    minor_version = models.PositiveSmallIntegerField()
    patch_version = models.PositiveSmallIntegerField()
    timestamp=models.DateTimeField(auto_now=False, auto_now_add=True)
    file=models.FileField(upload_to=version_filename_save)
    changelog=models.TextField(max_length=1000)

    def clean(self):
        '''Makes row checks only if model created first time and version didn didnt change'''
        #TODO: Move to utils
        if self.id is not None:
            original = VersionHistory.objects.get(id = self.id)
            if original.major_version == self.major_version and original.minor_version == self.minor_version and original.patch_version == self.patch_version:
                return

        try:
            if self.major_version+self.minor_version+self.patch_version == 0:
                raise ValidationError("Version can't be 0.0.0")
        except TypeError:
            raise ValidationError('Only numbers')

        if VersionHistory.objects.filter(entry=self.entry, major_version=self.major_version,
                                         minor_version=self.minor_version, patch_version=self.patch_version).exists():
            raise ValidationError("This version already exist")
        ##TODO: REFACTOR THIS TRASH!
        last_version = VersionHistory.objects.filter(entry=self.entry).first()
        if last_version:
            if (last_version.major_version>=self.major_version and last_version.minor_version>=self.minor_version and
                        last_version.patch_version>=self.patch_version):
                raise ValidationError('Version have to be greater than previous')

    class Meta:
        verbose_name_plural='version history'
        ordering = ('-major_version', '-minor_version', '-patch_version')
        get_latest_by = "timestamp"

    def version(self):
        return str(self.major_version)+'.'+str(self.minor_version)+'.'+str(self.patch_version)

    def __str__(self):
        return self.version()
