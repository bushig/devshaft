from crispy_forms.templatetags.crispy_forms_field import css_class
from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory, inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, Fieldset, Field
from mptt.forms import TreeNodeChoiceField

from .models import Entry, VersionHistory, EntryImage, Category


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = (
        'category', 'name', 'description', 'languages', 'frameworks', 'repository', 'site', 'license', 'entry_type',
        'github_releases', 'changelog', 'locked')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter name of asset'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe asset'}),
        }


class VersionForm(forms.ModelForm):
    field_order = ('entry', 'version', 'changelog', 'file')

    helper = FormHelper()
    helper.form_id = 'id-addVersionForm'
    helper.form_method = 'post'

    helper.add_input(Submit('submit', 'Submit'))

    helper.form_class = 'form-horizontal'
    # helper.form_show_labels=False
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        'entry', 'version', 'changelog', 'file'
    )

    class Meta:
        model = VersionHistory
        fields = ('version', 'file', 'changelog')
        widgets = {
            'version': forms.TextInput(attrs={'placeholder': 'v0.0.1'}),
            'changelog': forms.Textarea(attrs={'placeholder': 'Changelog'}),
            'file': forms.FileInput(attrs={'required': True}),
        }


class VersionFormEdit(forms.ModelForm):
    field_order = ('changelog', 'file')

    class Meta:
        model = VersionHistory
        fields = ('file', 'changelog')


class SearchForm(forms.Form):
    q = forms.CharField(max_length=120, required=False)
    category = TreeNodeChoiceField(Category.objects.all(), required=False)
    # o=forms.ChoiceField(choices=('version', 'Last updated'))
    field_order = ('q', 'category')

    class Meta:
        fields = ('q', 'category', 'o')
        # widgets = {'q': forms.TextInput(attrs={'help-block': "Type in asset name, description or creator's name"})}


class EntryImageForm(forms.ModelForm):
    class Meta:
        model = EntryImage
        fields = ('image', 'cropping')


# Edit entry images formset TODO:REFACTOR
EntryImageFormSet = inlineformset_factory(Entry, EntryImage, extra=5, max_num=5, form=EntryImageForm)
