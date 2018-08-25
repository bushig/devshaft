from django.db.models import Q
from django.forms.widgets import SelectMultiple, CheckboxSelectMultiple

import django_filters
from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField

from .models import Asset, Category
from .forms import SearchForm

class TreeeMultipleFilter(django_filters.MultipleChoiceFilter):
    field_class = TreeNodeMultipleChoiceField

#TODO: Move this somewhere else (forms)
class EntryFilter(django_filters.FilterSet):
    '''
    Filtering for Entries
    '''
    q=django_filters.CharFilter(method='filter_search', label='Search', help_text='You can search by asset name, description or asset creator')
    o = django_filters.OrderingFilter(fields=[('users_liked__count', 'likes'),
                                              ('updated', 'updated')])
    category = TreeeMultipleFilter(method='filter_category', queryset=Category.objects.all(), widget=SelectMultiple(attrs={'style': 'height:500px'}))
    class Meta:
        model = Asset
        form = SearchForm
        fields = ('q', 'category', 'languages', 'frameworks') #TODO: Rename category to c/ FIX ordering

    def filter_category(self, queryset, name, value):
        if value:
            value = value.get_descendants(include_self=True)
            return queryset.filter(category__in=value)
        return queryset

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value) | Q(user__username__iexact=value))

    #TODO: Greatly improve this to have fields search query(includes name, descript, user), category and tags


