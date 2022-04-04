from userprofile.models import Profile
from .models import Bug
from django import forms
from project.models import Project
from django.shortcuts import get_object_or_404
from constants.constants import DEVELOPER


class BugForm(forms.ModelForm):
  assigned_dev = forms.ChoiceField(choices=())
  class Meta:
    model = Bug
    fields = ('title', 'description', 'assigned_dev', 'deadline', 'type', 'screenshot')

  def __init__(self, *args, project_id, **kwargs):
    super(BugForm, self).__init__(*args, **kwargs)
    self.fields['assigned_dev'] = forms.ChoiceField(choices=self.get_choices(project_id))

  def get_choices(self, id):
    project = get_object_or_404(Project, id)
    devs = Profile.objects.filter(project=project).filter(designation=DEVELOPER)
    choices = ((-1, 'None'), )
    for dev in devs:
        choices = choices + ((dev.id, dev.user.get_full_name()),)
    return choices
