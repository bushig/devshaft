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
    o = django_filters.OrderingFilter(fields=[('-likes__count', 'likes'),
                                              ('-updated', 'updated')])
    class Meta:
        model = Framework
        fields = ('q', 'languages', 'target_platforms', 'editor_platforms', 'framework_type', 'is_2d', 'is_3d')

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value) | Q(user__username__iexact=value))

    #TODO: Greatly improve this to have fields search query(includes name, descript, user), category and tags


