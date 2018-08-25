from django.db.models import Q
from django.forms.widgets import SelectMultiple, CheckboxSelectMultiple

import django_filters
from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField

from .models import Framework


#TODO: Move this somewhere else (forms)
class FrameworkFilter(django_filters.FilterSet):
    '''
    Filtering for Entries
    '''
    q=django_filters.CharFilter(method='filter_search', label='Search', help_text='You can search by framework name, description or creator')
    o = django_filters.OrderingFilter(fields=[('likes', 'likes'),
                                              ('-updated', 'updated')])
    is_open_source = django_filters.BooleanFilter(method='is_open_source_filter', label='Is open source')
    class Meta:
        model = Framework
        fields = ('q', 'languages', 'target_platforms', 'editor_platforms', 'is_free', 'is_open_source',
                  'is_royalty_free', 'is_2d', 'is_3d')
    #TODO: switcher between Free as beer, Free as language, open_source
    def is_open_source_filter(self, queryset, name, value):
        if value is True:
            return queryset.exclude(repository_url__isnull=True)
        elif value is False:
            return queryset.filter(repository_url__isnull=True)
        else:
            return queryset

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value) | Q(user__username__iexact=value))

    #TODO: Greatly improve this to have fields search query(includes name, descript, user), category and tags


