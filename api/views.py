from xml.dom import NotFoundErr
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from project.models import Project
from userprofile.models import Profile
from bugs.models import Bug
from utilities.constants import DEVELOPER
from .serializers import ProjectSerializer, ProfileSerializer, BugSerializer
from utilities import MANAGER, QAENGINEER
from utilities.constants import BUG, FEATURE, NEW, INPROGRESS, COMPLETED


@api_view(["GET"])
def getProjectsList(request):
    if not request.user.is_authenticated:
        return Response(
            {"error_message": str("You must be signed in to access this page")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    profile = Profile.objects.get(user=request.user)
    if profile.designation not in (MANAGER, QAENGINEER):
        return Response(
            {
                "error_message": str(
                    "You must be a Manager or QAEngineer to access this page"
                )
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getUsersList(request, slug):

    if slug not in (DEVELOPER, QAENGINEER):
        return Response(
            {"error_message": str("No page found on requested URL")},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not request.user.is_authenticated:
        return Response(
            {"error_message": str("You must be signed in to access Employee List")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    profile = Profile.objects.get(user=request.user)
    if profile.designation != MANAGER:
        return Response(
            {"error_message": str("You must be a Manager to access Employee List")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    profile = Profile.objects.filter(designation=slug)
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getUsersList(request, slug):

    if slug not in (DEVELOPER, QAENGINEER):
        return Response(
            {"error_message": str("No page found on requested URL")},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not request.user.is_authenticated:
        return Response(
            {"error_message": str("You must be signed in to access Employee List")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    profile = Profile.objects.get(user=request.user)
    if profile.designation != MANAGER:
        return Response(
            {"error_message": str("You must be a Manager to access Employee List")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    profile = Profile.objects.filter(designation=slug)
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getBugsList(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response(
            {"error_message": str("You must be signed in to access this page")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    profile = Profile.objects.get(user=request.user)
    if profile.designation not in (MANAGER, QAENGINEER):
        return Response(
            {
                "error_message": str(
                    "You must be a Manager or QAEngineer to access this page"
                )
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    bugs = Bug.objects.all()

    if "slug" in kwargs and "filter" not in kwargs:
        if kwargs["slug"] not in (BUG, FEATURE, NEW, INPROGRESS, COMPLETED):
            return Response(
                {"error_message": str("No page found on requested URL")},
                status=status.HTTP_404_NOT_FOUND,
            )
        if kwargs["slug"] in (BUG, FEATURE):
            bugs = bugs.filter(type=kwargs["slug"])
        else:
            bugs = bugs.filter(type=kwargs["slug"])

    elif "filter" in kwargs:
        if kwargs["slug"] not in (BUG, FEATURE) or kwargs["filter"] not in (
            NEW,
            INPROGRESS,
            COMPLETED,
        ):
            return Response(
                {"error_message": str("No page found on requested URL")},
                status=status.HTTP_404_NOT_FOUND,
            )
        bugs = bugs.filter(type=kwargs["slug"]).filter(status=kwargs["filter"])
    serializer = BugSerializer(bugs, many=True)
    return Response(serializer.data)
