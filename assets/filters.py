import django_filters
from django.db.models import Q

from .models import Entry, Category,  Tag
from .forms import SearchForm

class EntryFilter(django_filters.FilterSet):
    '''
    Filtering for Entries
    '''
    q=django_filters.MethodFilter(action='filter_search', label='Search', help_text='You can search by asset name, description or asset creator')
    tags=django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), label='Tags', help_text='Shows asset if any of tags occurs in it')
    class Meta:
        model = Entry
        form = SearchForm
        fields = ('q', 'category', 'tags') #TODO: Rename tags filter to t and category to c/ FIX ordering
        order_by = (('likes','Most liked'),
                    ('version', 'Last updated'))

    def get_order_by(self, order_choice):
        if order_choice=='likes':
            return ['-entrylikes__count']
        elif order_choice=='version':
            return ['-versionhistory__timestamp__max'] #by most recent version
        return super(EntryFilter, self).get_order_by(order_choice)

    def filter_search(self, queryset, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value) | Q(user__username=value))

    #TODO: Greatly improve this to have fields search query(includes name, descript, user), category and tags
