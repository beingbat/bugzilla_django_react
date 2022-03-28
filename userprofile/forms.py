from random import choices
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from userprofile.models import Profile
from userprofile.models import USER_TYPES



class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

class ProfileForm(forms.ModelForm):

    designation = forms.ChoiceField(choices=USER_TYPES)

    class Meta:
        model = Profile
        fields = ('designation', )
