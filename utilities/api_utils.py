from rest_framework.response import Response
from rest_framework import status

from utilities import MANAGER

def check_authenticated(request):
    if not request.user.is_authenticated:
        return Response(
            {"error_message": str("You must be signed in to access this page")},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return False


def check_authorized(designation, list):

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


def check_manager(designation):
    if designation != MANAGER:
        return Response(
            {"error_message": str("You must be a Manager to access this page")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return True


def validate_user(request, list):
    response = check_authenticated(request)
    if response:
        return response

    from userprofile.models import Profile
    profile = Profile.objects.get(user=request.user)
    response = check_authorized(profile.designation, list)
    if response:
        return response
    return False
