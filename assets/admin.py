from django.contrib import admin

from image_cropping import ImageCroppingMixin
from reversion.admin import VersionAdmin

from .models import Entry,Category, VersionHistory, EntryImage, EntrySettings

# class VersionHistoryAdmin(admin.ModelAdmin):
#     # class Meta:
#     #     model=VersionHistory
#
#     fields = ('entry', 'version', 'timestamp', 'changelog')
#     list_display = ('entry', 'version')

class EntryAdmin(VersionAdmin):
    class Meta:
        model = Entry
    # fields = ('category', 'user', 'name', 'description')
    list_display = ('name', 'category', 'user', 'total_likes')

class EntryImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(Entry, EntryAdmin)
admin.site.register(Category)
admin.site.register(VersionHistory)
admin.site.register(EntryImage, EntryImageAdmin)
admin.site.register(EntrySettings)