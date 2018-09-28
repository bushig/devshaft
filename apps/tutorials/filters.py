from django.db.models import Q
from django.forms.widgets import SelectMultiple, CheckboxSelectMultiple
import taggit
import django_filters
from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField
import tagulous

from .models import Tutorial
from .forms import SearchForm




#TODO: Move this somewhere else (forms)
class TutorialFilter(django_filters.FilterSet):
    '''
    Filtering for Tutorials
    '''
    q=django_filters.CharFilter(method='filter_search', label='Search', help_text='You can search by tutorial name or description')
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tutorial.tags.tag_model.objects.all(), method='filter_tags')
    desc = django_filters.BooleanFilter(field_name=None)
    o = django_filters.OrderingFilter(fields=[('users_liked__count', 'likes'),
                                              ('updated', 'updated')])
    class Meta:
        model = Tutorial
        form = SearchForm
        fields = ('q', 'languages', 'frameworks', 'assets', 'desc', 'tags')

    #TODO: override qs property for search on all fields
    def filter_tags(self, queryset, name, value):
        print(queryset, name, value)
        tags = set()
        for tag in value:
            tags.add(tag)
            if self.desc:
                for t in tag.get_descendants():
                    tags.add(t)
        return queryset.filter(tags__in=tags).distinct()

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))

    #TODO: Greatly improve this to have fields search query(includes name, descript, user), category and tags


