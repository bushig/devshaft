from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory, inlineformset_factory

from .models import Framework, FrameworkImage


class FrameworkForm(forms.ModelForm):
    class Meta:
        model = Framework
        fields = (
        'title', 'description', 'license', 'is_2d', 'is_3d', 'languages', 'editor_platforms', 'target_platforms',
        'site', 'repository_url')


class FrameworkImageForm(forms.ModelForm):
    class Meta:
        model = FrameworkImage
        fields = ('image', 'cropping')


# Edit entry images formset TODO:REFACTOR
FrameworkImageFormSet = inlineformset_factory(Framework, FrameworkImage, extra=5, max_num=5, form=FrameworkImageForm)