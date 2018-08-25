from django.contrib import admin

from image_cropping import ImageCroppingMixin
from reversion.admin import VersionAdmin

from .models import Asset, Category, Release, AssetImage, ReleaseUpload


class ReleaseInline(admin.TabularInline):
    model = Release
    fields = ('asset', 'version', 'timestamp', 'changelog')


class AssetImageInline(ImageCroppingMixin, admin.StackedInline):
    model = AssetImage


class ReleaseUploadAdminInline(admin.StackedInline):
    model = ReleaseUpload


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    class Meta:
        model = Release

    inlines = (ReleaseUploadAdminInline,)
    list_display = ('asset', 'version', 'timestamp')


@admin.register(Asset)
class AssetAdmin(VersionAdmin):
    inlines = (AssetImageInline, ReleaseInline)
    list_display = ('name', 'category', 'user', 'total_likes')
    class Meta:
        model = Asset



admin.site.register(Category)
