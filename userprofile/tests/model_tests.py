from django.test import TestCase
from django.contrib.auth.models import User
from userprofile.models import Profile
from project.models import Project
from utilities import USER_TYPES, MANAGER


class UserProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            first_name="Big", last_name="Bob", username="test_user"
        )
        Profile.objects.create(user=user)

    def test_only_single_profile_linked_with_user(self):
        user = User.objects.get(username="test_user")
        profile_count = Profile.objects.filter(user=user).count()
        self.assertEqual(profile_count, 1)

    def test_designation_choices(self):
        profile = Profile.objects.get(user=User.objects.get(username="test_user"))
        choices = profile._meta.get_field("designation").choices
        self.assertEqual(
            choices,
            USER_TYPES + ((MANAGER, "Manager"),),
        )

    def test_project_foreign_key_name(self):
        project = Project(name="Test Project")
        project.save()
        profile = Profile.objects.get(user=User.objects.get(username="test_user"))
        profile.project = project
        profile.save()
        self.assertEqual(profile.project.name, "Test Project")

    def test_profile_object_name(self):
        profile = Profile.objects.get(user=User.objects.get(username="test_user"))
        expected_object_name = f"{profile.user.username}"
        self.assertEqual(str(profile), expected_object_name)

    def test_get_absolute_url(self):
        profile = Profile.objects.get(user=User.objects.get(username="test_user"))
        self.assertEqual(profile.get_absolute_url(), f"/users/{profile.user.id}")
