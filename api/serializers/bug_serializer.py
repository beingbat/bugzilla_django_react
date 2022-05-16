from rest_framework import serializers
from bugs.models import Bug
from api.serializers.profile_serializer import UserSerializer

class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields = ['uuid', 'title', 'type', 'status', 'creator', 'assigned_to', 'project']
