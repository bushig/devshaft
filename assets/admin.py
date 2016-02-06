from django.contrib import admin
from .models import Entry,Categoty, VersionHistory

# class VersionHistoryAdmin(admin.ModelAdmin):
#     # class Meta:
#     #     model=VersionHistory
#
#     fields = ('entry', 'version', 'timestamp', 'changelog')
#     list_display = ('entry', 'version')


admin.site.register(Entry)
admin.site.register(Categoty)
admin.site.register(VersionHistory)
