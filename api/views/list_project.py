from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from project.models import Project
from userprofile.models import Profile
from api.serializers import ProjectSerializer
from utilities import MANAGER, QAENGINEER


class ListProjects(APIView):
    def get(self, request, format=None):
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
