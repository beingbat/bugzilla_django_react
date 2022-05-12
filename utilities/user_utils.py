from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from .constants import MANAGER, USER_TYPES, QAENGINEER


def get_designation(profile):
    if profile.designation == MANAGER:
        return "Manager"
    else:
        return dict(USER_TYPES).get(profile.designation)


def is_manager(user):
    from userprofile.models import Profile

    current_user = get_object_or_404(Profile, user=user)
    return True if current_user.designation == MANAGER else False


def get_user_profile(user):
    from userprofile.models import Profile

    return get_object_or_404(Profile, user=user)


def get_user_profile_by_id(user_id):
    from userprofile.models import Profile

    user = get_object_or_404(User, id=user_id)
    return get_object_or_404(Profile, user=user)
