from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

from userprofile.models import Profile
from api.serializers import ProfileSerializer

from utilities import MANAGER, QAENGINEER, DEVELOPER, validate_user


class ProfileCollectionAPIView(APIView):
    def get(self, request, *args, **kwargs):

        if "slug" not in kwargs:
            return Response(
                {"error_message": str("No page found on requested URL")},
                status=status.HTTP_404_NOT_FOUND,
            )

        if kwargs["slug"] not in (DEVELOPER, QAENGINEER):
            return Response(
                {"error_message": str("No page found on requested URL")},
                status=status.HTTP_404_NOT_FOUND,
            )

        validate_user(request=request, list=(MANAGER, QAENGINEER))

        profile = Profile.objects.filter(designation=kwargs["slug"])
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)
