from django.contrib import admin
import tagulous

from image_cropping import ImageCroppingMixin
from reversion.admin import VersionAdmin
from markdownx.admin import MarkdownxModelAdmin

from apps.tutorials.models import Tutorial


@admin.register(Tutorial)
class TutorialAdmin(MarkdownxModelAdmin):
    list_display = ('name', 'user')
    search_fields = ['name', 'user__username']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    class Meta:
        model = Tutorial

tagulous.admin.register(Tutorial.tags)