from django.test import TestCase

from django.contrib.auth.models import User
from userprofile.models import Profile

from project.tests.factories.project import ProjectFactory
from userprofile.tests.factories.profile import ProfileFactory
from userprofile.tests.factories.user import UserFactory

from utilities import USER_TYPES, MANAGER


class UserProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = UserFactory()
        profile = ProfileFactory(user=user, project=None)
        # print(f"User Details: usernamae: {user.username}, email: {user.email}, profile designation: {profile.designation}")

    def setUp(self):
        self.user = User.objects.last()
        self.profile = Profile.objects.last()

    def test_only_single_profile_linked_with_user(self):
        profile_count = Profile.objects.filter(user=self.user).count()
        self.assertEqual(profile_count, 1)

    def test_designation_choices(self):
        choices = self.profile._meta.get_field("designation").choices
        self.assertEqual(
            choices,
            USER_TYPES + ((MANAGER, "Manager"),),
        )

    def test_project_foreign_key_name(self):
        project = ProjectFactory()
        project.save()
        self.profile.project = project
        self.profile.save()
        # print(f"\nProject Added: Name: {self.profile.project.name}\nDescription: {self.profile.project.description}\n")
        self.assertEqual(self.profile.project.name, project.name)

    def test_profile_object_name(self):
        expected_object_name = f"{self.profile.user.username}"
        self.assertEqual(str(self.profile), expected_object_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.profile.get_absolute_url(), f"/users/{self.profile.user.id}")
