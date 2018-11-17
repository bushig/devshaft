from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import License

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin


class NewsEntryAdmin(EntryAdmin):
  # In our case we put the gallery field
  # into the 'Content' fieldset
  fieldsets = EntryAdmin.fieldsets + (
    (_('Connected items'), {
      'fields': ('frameworks', 'assets', 'series'),
      'classes': ('collapse', 'collapse-closed')}),)


admin.site.register(Entry, NewsEntryAdmin)

admin.site.register(License)
