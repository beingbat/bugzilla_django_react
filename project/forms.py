from django import forms
from django.shortcuts import get_object_or_404

from .models import Project
from userprofile.models import Profile

from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):

    name = forms.CharField(max_length=50)
    description = forms.TextInput()

    class Meta:
        model = Project
        fields = ('name', 'description',)


class ProjectChooseForm(forms.ModelForm):
    projects_field = forms.ChoiceField(choices=())

    class Meta:
        model = Project
        fields = ('projects_field', )

    def __init__(self, *args, pk, **kwargs):
        super(ProjectChooseForm, self).__init__(*args, **kwargs)
        profile = get_object_or_404(
            Profile, user=get_object_or_404(User, id=pk))
        if profile.project:
            p_id = profile.project.id
        else:
            p_id = -1

        self.fields['projects_field'] = forms.ChoiceField(
            choices=self.get_choices(), initial=str(p_id))

    def get_choices(self):

        projects = Project.objects.all()
        choices = ((-1, 'None'), )
        for project in projects:
            choices = choices + ((project.id, project.name),)
        return choices
