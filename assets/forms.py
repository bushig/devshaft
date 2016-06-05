from crispy_forms.templatetags.crispy_forms_field import css_class
from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory, inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, Fieldset, Field


from .models import Entry, VersionHistory, EntryImage, Category


class EntryForm(forms.ModelForm):
    field_order = ['category', 'name', 'description']

    helper = FormHelper()
    helper.form_id = 'id-addEntryForm'
    helper.form_method = 'post'
    helper.form_action = 'assets:add_entry'

    helper.add_input(Submit('submit', 'Submit'))

    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        'category',
        'name',
        'description',
    )


    class Meta:
        model=Entry
        fields=('category', 'name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter name of asset'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe asset'}),
        }


class VersionForm(forms.ModelForm):
    field_order = ('entry', 'major_version', 'minor_version', 'patch_version', 'changelog', 'file')

    helper = FormHelper()
    helper.form_id = 'id-addVersionForm'
    helper.form_method = 'post'

    helper.add_input(Submit('submit', 'Submit'))


    helper.form_class = 'form-horizontal'
    # helper.form_show_labels=False
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        'entry', 'major_version', 'minor_version', 'patch_version', 'changelog', 'file'
    )

    class Meta:
        model = VersionHistory
        fields = ('entry', 'major_version', 'minor_version', 'patch_version', 'file', 'changelog')
        widgets = {
            'entry': forms.HiddenInput(),
            'major_version': forms.TextInput(attrs={'placeholder': 'Major'}),
            'minor_version': forms.TextInput(attrs={'placeholder': 'Minor'}),
            'patch_version': forms.TextInput(attrs={'placeholder': 'Patch'}),
            'changelog': forms.Textarea(attrs={'placeholder': 'Changelog'}),
        }
class VersionFormEdit(forms.ModelForm):
    field_order = ('changelog', 'file')
    class Meta:
        model = VersionHistory
        fields = ('file', 'changelog')

class SearchForm(forms.Form):
    q=forms.CharField(max_length=120, required=False)
    category=forms.ModelChoiceField(Category.objects.all(), required=False)
    o=forms.ChoiceField(choices=('version', 'Last updated'))
    field_order = ('q', 'category', 'o')

    helper = FormHelper()
    helper.form_id = 'id-searchForm'
    helper.form_method = 'get'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        'q', 'category', 'o', Submit('', 'Search', css_class='btn-success')
    )

    class Meta:
        fields = ('q', 'category', 'tags', 'o')
        # widgets = {'q': forms.TextInput(attrs={'help-block': "Type in asset name, description or creator's name"})}



#Edit entry images formset TODO:REFACTOR
EntryImageFormSet=inlineformset_factory(Entry, EntryImage, fields=('image',), extra=5, max_num=5)