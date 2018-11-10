from crispy_forms.templatetags.crispy_forms_field import css_class
from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory, inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, Fieldset, Field
from mptt.forms import TreeNodeChoiceField

from .models import Asset, Release, AssetImage, Category, ReleaseUpload


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = (
        'category', 'name', 'description', 'languages', 'frameworks', 'repository', 'site', 'license')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter name of asset'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe asset'}),
        }


class ReleaseForm(forms.ModelForm):
    field_order = ('version', 'changelog')

    helper = FormHelper()
    helper.form_id = 'id-addVersionForm'
    helper.form_method = 'post'

    helper.add_input(Submit('submit', 'Submit'))

    helper.form_class = 'form-horizontal'
    # helper.form_show_labels=False
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        'version', 'changelog', 'timestamp'
    )

    class Meta:
        model = Release
        fields = ('version', 'changelog', 'timestamp')
        widgets = {
            'version': forms.TextInput(attrs={'placeholder': 'v0.0.1'}),
            'changelog': forms.Textarea(attrs={'placeholder': 'Changelog'}),
        }


class ReleaseFormEdit(forms.ModelForm):
    field_order = ('changelog',)
    #TODO: add ReleaseUploads forms
    class Meta:
        model = Release
        fields = ('changelog',)


class SearchForm(forms.Form):
    q = forms.CharField(max_length=120, required=False)
    category = TreeNodeChoiceField(Category.objects.all(), required=False)
    # o=forms.ChoiceField(choices=('version', 'Last updated'))
    field_order = ('q', 'category')

    class Meta:
        fields = ('q', 'category', 'o')
        # widgets = {'q': forms.TextInput(attrs={'help-block': "Type in asset name, description or creator's name"})}


class AssetImageForm(forms.ModelForm):
    class Meta:
        model = AssetImage
        fields = ('image', 'cropping')


class ReleaseUploadForm(forms.ModelForm):
    class Meta:
        model = ReleaseUpload
        fields = ('file', 'note')


# Edit entry images formset TODO:REFACTOR
EntryImageFormSet = inlineformset_factory(Asset, AssetImage, extra=5, max_num=5, form=AssetImageForm)
ReleaseUploadsFormSet = inlineformset_factory(Release, ReleaseUpload, extra=3, max_num=3, form=ReleaseUploadForm)