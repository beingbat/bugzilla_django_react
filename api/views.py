from xml.dom import NotFoundErr
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from project.models import Project
from userprofile.models import Profile
from utilities.constants import DEVELOPER
from .serializers import ProjectSerializer, ProfileSerializer
from utilities import MANAGER, QAENGINEER

@api_view(['GET'])
def getProjectsList(request):
    if not request.user.is_authenticated:
        return Response({'error_message': str("You must be signed in to access this page")}, status=status.HTTP_401_UNAUTHORIZED)


    profile = Profile.objects.get(user=request.user)
    if profile.designation not in  (MANAGER, QAENGINEER):
        return Response({'error_message': str("You must be a Manager or QAEngineer to access this page")}, status=status.HTTP_401_UNAUTHORIZED)


    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUsersList(request, slug):

    if slug not in (DEVELOPER, QAENGINEER):
        return Response({'error_message': str("No page found on requested URL")}, status=status.HTTP_404_NOT_FOUND)

    if not request.user.is_authenticated:
        return Response({'error_message': str("You must be signed in to access Employee List")}, status=status.HTTP_401_UNAUTHORIZED)


    profile = Profile.objects.get(user=request.user)
    if profile.designation != MANAGER:
        return Response({'error_message': str("You must be a Manager to access Employee List")}, status=status.HTTP_401_UNAUTHORIZED)


    profile = Profile.objects.filter(designation=slug)
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)


