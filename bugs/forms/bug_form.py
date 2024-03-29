from django.shortcuts import get_object_or_404

from django import forms

from utilities import *
from userprofile.models.profile_model import Profile
from project.models.project_model import Project
from bugs.models.bug_model import Bug


class BugForm(forms.ModelForm):
    assigned_dev = forms.ChoiceField(choices=())
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), initial="Due By"
    )

    class Meta:
        model = Bug
        fields = ("title", "description", "assigned_dev", "deadline", "screenshot")

    def __init__(self, *args, count_allowed, project_id, **kwargs):
        super(BugForm, self).__init__(*args, **kwargs)
        self.fields["assigned_dev"] = forms.ChoiceField(
            label="Assign a Developer ", choices=self.get_choices(project_id)
        )
        self.initial["deadline"] = self.instance.deadline.isoformat()

        self.count_allowed = count_allowed
        self.project_id = project_id

    def clean(self):
        if self.cleaned_data.get("title"):
            same_count = (
                Bug.objects.filter(title=self.cleaned_data.get("title"))
                .filter(project=self.project_id)
                .count()
            )

            if same_count > self.count_allowed:
                self.add_error("title", "Bug name should be unique in a project")

    def get_choices(self, id):
        project = get_object_or_404(Project, id=id)
        devs = Profile.objects.filter(project=project).filter(designation=DEVELOPER)
        choices = ((-1, "None"),)
        for dev in devs:
            dev_id = str(dev.user.id) + ": " + str(dev.user.get_full_name())
            choices = choices + ((dev.user.id, dev_id),)
        return choices
