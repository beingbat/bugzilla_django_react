from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from userprofile.models.profile import Profile

from constants.constants import USER_TYPES


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)


class ProfileForm(forms.ModelForm):

    designation = forms.ChoiceField(choices=USER_TYPES)

    class Meta:
        model = Profile
        fields = ('designation', )
