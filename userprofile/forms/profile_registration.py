from django import forms

from userprofile.models import Profile

from utilities import USER_TYPES


class ProfileForm(forms.ModelForm):

    designation = forms.ChoiceField(choices=USER_TYPES)

    class Meta:
        model = Profile
        fields = ('designation', )
