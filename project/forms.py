from django import forms
from .models import *

class ProjectForm(forms.ModelForm):

    name = forms.CharField(max_length=50)
    description = forms.TextInput()

    class Meta:
        model = Project
        fields = ('name', 'description',)
