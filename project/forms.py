from django import forms
from .models import *

class ProjectForm(forms.ModelForm):

    name = forms.CharField(max_length=50)
    description = forms.TextInput()

    class Meta:
        model = Project
        fields = ('name', 'description',)



class ProjectChooseForm(forms.ModelForm):
    projects = Project.objects.all()
    choicess = ((-1, 'None'), )
    for project in projects:
        print("**********", project)
        choicess = choicess + ((project.id, project.name),)
    projects_field = forms.ChoiceField(choices=choicess)
    print(choicess)

    class Meta:
        model = Project
        fields = ('projects_field', )
