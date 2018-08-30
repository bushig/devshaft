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
    list_display = ('name', 'category', 'user', 'likes_count_admin')
    search_fields = ['name', 'user__username']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


    def likes_count_admin(self, obj):
        return obj.users_liked__count

    def username(self, obj):
        return obj.user

    class Meta:
        model = Asset



admin.site.register(Category)
