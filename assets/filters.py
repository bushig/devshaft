import django_filters

from .models import Entry, Category

class EntryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(max_length=120, lookup_type='icontains', label='Name', required=False) #search query
    # c = django_filters.ModelMultipleChoiceFilter(queryset = Category.objects.all(), label='Categories') #category
    class Meta:
        model = Entry
        exclude = ()
    #TODO: Greatly improve this to have fields search query(includes name, descript, user), category and tags
