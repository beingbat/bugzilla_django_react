from django import forms

from project.models.project import Project


class ProjectForm(forms.ModelForm):

    name = forms.CharField(max_length=50)
    description = forms.TextInput()

    class Meta:
        model = Project
        fields = ('name', 'description',)
