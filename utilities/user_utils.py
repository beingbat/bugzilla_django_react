from django.shortcuts import get_object_or_404

import userprofile.models as Profile
from django.contrib.auth.models import User
from .constants import MANAGER, USER_TYPES


def get_designation(profile):
    if profile.designation == MANAGER:
        return "Manager"
    else:
        return dict(USER_TYPES).get(profile.designation)


def is_manager(user):
    current_user = get_object_or_404(Profile, user=user)
    return True if current_user.designation == MANAGER else False


def get_user_profile(user):
    return get_object_or_404(Profile, user=user)


def get_user_profile_by_id(user_id):
    user = get_object_or_404(User, id=user_id)
    return get_object_or_404(Profile, user=user)
