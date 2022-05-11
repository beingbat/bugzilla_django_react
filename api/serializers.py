from rest_framework import serializers
from project.models import Project
from userprofile.models.profile_model import Profile
from django.contrib.auth.models import User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'designation', 'project']
        depth = 1
