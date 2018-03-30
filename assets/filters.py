from django.db.models import Q

import django_filters

from .models import Entry
from .forms import SearchForm

#TODO: Move this somewhere else (forms)
class EntryFilter(django_filters.FilterSet):
    '''
    Filtering for Entries
    '''
    q=django_filters.CharFilter(method='filter_search', label='Search', help_text='You can search by asset name, description or asset creator')
    # o = django_filters.OrderingFilter(fields=[] )
    class Meta:
        model = Entry
        # form = SearchForm
        fields = ('q', 'category') #TODO: Rename category to c/ FIX ordering
        order_by = (('version', 'Last updated'),
                    ('likes','Most liked'))

    def get_order_by(self, order_choice):
        if order_choice=='likes':
            return ['-users_liked__count']
        elif order_choice=='version':
            return ['-versionhistory__timestamp__max'] #by most recent version
        return super(EntryFilter, self).get_order_by(order_choice)

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value) | Q(user__username=value))

    #TODO: Greatly improve this to have fields search query(includes name, descript, user), category and tags


