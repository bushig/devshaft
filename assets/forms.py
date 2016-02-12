from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory, inlineformset_factory

from .models import Entry, VersionHistory, EntryImage


class EntryForm(forms.ModelForm):
    # name=forms.CharField(max_length=120, help_text=)
    field_order = ['category', 'name', 'description']
    class Meta:
        model=Entry
        fields=('category', 'name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name of asset'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe asset'}),
        }


class VersionForm(forms.ModelForm):
    field_order = ('major_version', 'minor_version', 'patch_version', 'changelog', 'file')
    class Meta:
        model = VersionHistory
        fields = ('major_version', 'minor_version', 'patch_version', 'file', 'changelog')
        widgets = {
            'major_version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Major'}),
            'minor_version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Minor'}),
            'patch_version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patch'}),
            'changelog': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Changelog'}),
        }

#Edit entry images formset TODO:REFACTOR
EntryImageFormSet=inlineformset_factory(Entry, EntryImage, fields=('image',), extra=1)