from django import forms

from .models import Entry, VersionHistory


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
    class Meta:
        model = VersionHistory
        fields = ('version', 'changelog', 'file')