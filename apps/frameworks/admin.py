from django.contrib import admin

from reversion.admin import VersionAdmin
from image_cropping import ImageCroppingMixin

from .models import Platform, Framework, FrameworkImage

class FrameworkImageInline(admin.StackedInline):
    model = FrameworkImage

class FrameworkAdmin(admin.ModelAdmin):
    readonly_fields = ('repo_stars', 'repo_forks', 'repo_description', 'repo_updated', 'last_commit', 'commits')
    inlines = (FrameworkImageInline, )

admin.site.register(Platform)
admin.site.register(Framework, FrameworkAdmin)