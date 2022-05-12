from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from api.serializers import BugSerializer
from userprofile.models import Profile
from bugs.models import Bug
from utilities import MANAGER, QAENGINEER, BUG, FEATURE, NEW, INPROGRESS, COMPLETED
from .api_utils import validate_user


class BugCollectionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        response = validate_user(
            request,
            (
                QAENGINEER,
                MANAGER,
            ),
        )
        if response:
            return response
        bugs = Bug.objects.all()

        if "slug" in kwargs and "filter" not in kwargs:
            if kwargs["slug"] not in (BUG, FEATURE, NEW, INPROGRESS, COMPLETED):
                return Response(
                    {"error_message": str("No page found on requested URL")},
                    status=status.HTTP_404_NOT_FOUND,
                )
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
