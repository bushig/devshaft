from django.db.models import Q
from django.forms.widgets import SelectMultiple, CheckboxSelectMultiple
import taggit
import django_filters
from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField
import tagulous

from .models import Tutorial
from .forms import SearchForm


TAGS_DESC_CHOICES = (
    ('0', 'No'),
    ('1', 'Yes')
)

#TODO: Move this somewhere else (forms)
class TutorialFilter(django_filters.FilterSet):
    '''
    Filtering for Tutorials
    '''
    q = django_filters.CharFilter(method='filter_search', label='Search', help_text='You can search by tutorial name or description')
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tutorial.tags.tag_model.objects.all(), method='filter_tags')
    desc_tags = django_filters.ChoiceFilter(label='Tags with descendants', method='filter_desc_tags',
                                            choices=TAGS_DESC_CHOICES, empty_label=None)
    o = django_filters.OrderingFilter(fields=[('users_liked__count', 'likes'),
                                              ('updated', 'updated')])
    class Meta:
        model = Tutorial
        #form = SearchForm
        fields = ('q', 'languages', 'frameworks', 'assets', 'tags', 'desc_tags', )

    #TODO: override qs property for search on all fields
    def filter_tags(self, queryset, name, value):
        return queryset

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
        else:
            return queryset

    def filter_desc_tags(self, queryset, name, value):
        return queryset

    @property
    def qs(self):
        # Just bunch of hacks
        parent = super(TutorialFilter, self).qs
        desc_tags = self.data.get('desc_tags', '0')
        print(self.data.get('tags', []))
        tags = set()
        for tag_id in self.data.get('tags', []):
            tag = Tutorial.tags.tag_model.objects.get(id=tag_id)
            tags.add(tag)
            if str(desc_tags) == '1':
                for t in tag.get_descendants():
                    tags.add(t)
        if len(tags) > 0:
            return parent.filter(tags__in=tags).distinct()
        else:
            return parent
    #TODO: Greatly improve this to have fields search query(includes name, descript, user), category and tags


