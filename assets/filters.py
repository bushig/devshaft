from django.db.models import Q

import django_filters
from mptt.forms import TreeNodeChoiceField

from .models import Entry, Category
from .forms import SearchForm

#TODO: Move this somewhere else (forms)
class EntryFilter(django_filters.FilterSet):
    '''
    Filtering for Entries
    '''
    q=django_filters.CharFilter(method='filter_search', label='Search', help_text='You can search by asset name, description or asset creator')
    o = django_filters.OrderingFilter(fields=[('users_liked__count', 'likes'),
                                              ('versionhistory__timestamp__max', 'updated')])
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())
    class Meta:
        model = Entry
        form = SearchForm
        fields = ('q', 'category') #TODO: Rename category to c/ FIX ordering

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value) | Q(user__username=value))

    #TODO: Greatly improve this to have fields search query(includes name, descript, user), category and tags


