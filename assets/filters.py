import django_filters
from django.db.models import Q

from .models import Entry, Category

class EntryFilter(django_filters.FilterSet):
    q=django_filters.MethodFilter(action='filter_search', label='Search')
    class Meta:
        model = Entry
        fields = ('q', 'category')

    def filter_search(self, queryset, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value) | Q(user__username=value))

    #TODO: Greatly improve this to have fields search query(includes name, descript, user), category and tags
