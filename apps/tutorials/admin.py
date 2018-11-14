from django.contrib import admin
import tagulous

from image_cropping import ImageCroppingMixin
from reversion.admin import VersionAdmin
from markdownx.admin import MarkdownxModelAdmin

from apps.tutorials.models import Tutorial, Series, TutorialMembership

class TutorialInline(admin.StackedInline):
    model = TutorialMembership


@admin.register(Tutorial)
class TutorialAdmin(MarkdownxModelAdmin):
    list_display = ('name', 'user')
    search_fields = ['name', 'user__username']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    class Meta:
        model = Tutorial


@admin.register(Series)
class SeriesAdmin(MarkdownxModelAdmin):
    list_display = ('name', 'user')
    search_fields = ['name', 'user__username']
    inlines = (TutorialInline, )
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    class Meta:
        model = Series

tagulous.admin.register(Tutorial.tags)