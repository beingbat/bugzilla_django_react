from rest_framework.response import Response
from rest_framework import status

from userprofile.models import Profile
from utilities import MANAGER, QAENGINEER, BUG, FEATURE, NEW, INPROGRESS, COMPLETED


def is_not_user_authenticated(request):
    if not request.user.is_authenticated:
        return Response(
            {"error_message": str("You must be signed in to access this page")},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return False


def is_not_authorized(designation, list):

    if designation not in list:
        return Response(
            {
                "error_message": str(
                    "You must be a Manager or QAEngineer to access this page"
                )
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return False


def is_not_manager(designation):
    if designation != MANAGER:
        return Response(
            {"error_message": str("You must be a Manager to access this page")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return True


def validate_user(request, list):
    response = is_not_user_authenticated(request)
    if response:
        return response
    profile = Profile.objects.get(user=request.user)
    response = is_not_authorized(profile.designation, list)
    if response:
        return response
    return False
