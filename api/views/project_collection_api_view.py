from rest_framework.views import APIView
from rest_framework.response import Response

from project.models import Project
from api.serializers import ProjectSerializer
from utilities import MANAGER, validate_user


class ProjectCollectionAPIView(APIView):
    def get(self, request, format=None):
        response = validate_user(request, (MANAGER,))
        if response:
            return response
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
