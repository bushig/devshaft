from django.contrib import admin

from .models import Entry,Category, VersionHistory, EntryImage

# class VersionHistoryAdmin(admin.ModelAdmin):
#     # class Meta:
#     #     model=VersionHistory
#
#     fields = ('entry', 'version', 'timestamp', 'changelog')
#     list_display = ('entry', 'version')

class EntryAdmin(admin.ModelAdmin):
    class Meta:
        model = Entry
    fields = ('category', 'user', 'name', 'description')
    list_display = ('name', 'category', 'user', 'total_likes')

admin.site.register(Entry, EntryAdmin)
admin.site.register(Category)
admin.site.register(VersionHistory)
admin.site.register(EntryImage)
