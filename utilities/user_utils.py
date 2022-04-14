from django.shortcuts import get_object_or_404

from userprofile.models import Profile
from django.contrib.auth.models import User

from . import constants

def get_designation(profile):
    if profile.designation == constants.MANAGER:
        return 'Manager'
    else:
        return dict(constants.USER_TYPES).get(profile.designation)


def is_manager(user):
    current_user = get_object_or_404(Profile, user=user)
    return True if current_user.designation == constants.MANAGER else False


def get_user_profile(user):
    return get_object_or_404(Profile, user=user)


def get_user_profile_by_id(user_id):
    user = get_object_or_404(User, id=user_id)
    return get_object_or_404(Profile, user=user)
