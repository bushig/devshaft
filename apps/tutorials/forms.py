from django import forms
from django.forms.models import inlineformset_factory

from apps.tutorials.models import Tutorial, Series, TutorialMembership


class SearchForm(forms.Form):
    q = forms.CharField(max_length=120, required=False)
    # o=forms.ChoiceField(choices=('version', 'Last updated'))
    field_order = ('q',)

    class Meta:
        fields = ('q', 'o')
        # widgets = {'q': forms.TextInput(attrs={'help-block': "Type in asset name, description or creator's name"})}


class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ('languages', 'frameworks', 'assets', 'tags', 'name', 'short_description', 'content', 'url',
                  'credit_note', 'image')


class TutorialEditForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ('languages', 'frameworks', 'assets', 'tags', 'name', 'short_description', 'content', 'url',
                  'credit_note', 'image', 'cropping')


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ('languages', 'frameworks', 'assets', 'tags', 'name', 'short_description', 'content',
                  'credit_note', 'image')


class TutorialMembershipForm(forms.ModelForm):
    class Meta:
        model = TutorialMembership
        fields = ('tutorial', 'order')


TutorialFormSet = inlineformset_factory(Series, TutorialMembership, extra=15, max_num=20, form=TutorialMembershipForm)
