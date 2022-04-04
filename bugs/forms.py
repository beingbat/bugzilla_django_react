from mimetypes import init
from tabnanny import verbose
from userprofile.models import Profile
from .models import Bug
from django import forms
from project.models import Project
from django.shortcuts import get_object_or_404
from constants.constants import DEVELOPER
from django.utils.timezone import now
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class BugForm(forms.ModelForm):
  assigned_dev = forms.ChoiceField(choices=())
  deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial="Due By")
  class Meta:
    model = Bug
    fields = ('title', 'description', 'assigned_dev', 'deadline', 'type', 'screenshot')
    widgets = {
          'deadline': DateInput(attrs={'type': 'date'})
      }

  def __init__(self, *args, project_id, **kwargs):
    super(BugForm, self).__init__(*args, **kwargs)
    self.fields['assigned_dev'] = forms.ChoiceField(label="Assign a Developer ", choices=self.get_choices(project_id))
    self.initial['deadline'] = self.instance.deadline.isoformat()

  def get_choices(self, id):
    project = get_object_or_404(Project, id=id)
    devs = Profile.objects.filter(project=project).filter(designation=DEVELOPER)
    choices = ((-1, 'None'), )
    for dev in devs:
        choices = choices + ((dev.user.id, dev.user.get_full_name()),)
    return choices
