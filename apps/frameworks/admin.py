from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import Platform, Framework

class FrameworkAdmin(VersionAdmin):
    pass

admin.site.register(Platform)
admin.site.register(Framework, FrameworkAdmin)