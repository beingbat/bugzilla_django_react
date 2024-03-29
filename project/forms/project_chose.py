
from django import forms
from django.shortcuts import get_object_or_404

from project.models import Project
from userprofile.models import Profile

from django.contrib.auth.models import User


class ProjectChooseForm(forms.ModelForm):
    projects_field = forms.ChoiceField(choices=())

    class Meta:
        model = Project
        fields = ('projects_field', )

    def __init__(self, *args, pk, **kwargs):
        super(ProjectChooseForm, self).__init__(*args, **kwargs)
        self.profile = get_object_or_404(
            Profile, user=get_object_or_404(User, id=pk))
        if self.profile.project:
            p_id = self.profile.project.id
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
