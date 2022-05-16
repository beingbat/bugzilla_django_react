from rest_framework import serializers
from bugs.models import Bug


class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields = "__all__"
