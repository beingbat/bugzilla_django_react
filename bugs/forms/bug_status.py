from django.shortcuts import get_object_or_404

from django import forms

from utilities import *
from bugs.models.bug import Bug


class BugStatusForm(forms.ModelForm):
    status = forms.ChoiceField(choices=())

    class Meta:
        model = Bug
        fields = ('status', )

    def __init__(self, *args, pk, **kwargs):
        super(BugStatusForm, self).__init__(*args, **kwargs)
        bug = get_object_or_404(Bug, uuid=pk)
        self.fields['status'] = forms.ChoiceField(
            choices=self.get_choices(bug.type), initial=bug.status)

    def get_choices(self, type):
        if type == FEATURE:
            return FEATURE_STATUS
        else:
            return BUG_STATUS
