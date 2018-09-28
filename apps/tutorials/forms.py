from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(max_length=120, required=False)
    # o=forms.ChoiceField(choices=('version', 'Last updated'))
    field_order = ('q',)

    class Meta:
        fields = ('q', 'o')
        # widgets = {'q': forms.TextInput(attrs={'help-block': "Type in asset name, description or creator's name"})}
