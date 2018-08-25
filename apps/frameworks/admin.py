from django.contrib import admin

from reversion.admin import VersionAdmin
from image_cropping import ImageCroppingMixin

from .models import Platform, Framework, FrameworkImage

class FrameworkImageInline(admin.StackedInline):
    model = FrameworkImage

class FrameworkAdmin(VersionAdmin):
    inlines = (FrameworkImageInline, )

admin.site.register(Platform)
admin.site.register(Framework, FrameworkAdmin)