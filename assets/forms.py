from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory, inlineformset_factory

from .models import Entry, VersionHistory, EntryImage


class EntryForm(forms.ModelForm):
    field_order = ['category', 'name', 'description']
    class Meta:
        model=Entry
        fields=('category', 'name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter name of asset'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe asset'}),
        }


class VersionForm(forms.ModelForm):
    field_order = ('entry', 'major_version', 'minor_version', 'patch_version', 'changelog', 'file')
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

#Edit entry images formset TODO:REFACTOR
EntryImageFormSet=inlineformset_factory(Entry, EntryImage, fields=('image',), extra=5, max_num=5)