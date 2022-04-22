from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from userprofile.models import Profile

from project.tests.factories.project import ProjectFactory
from userprofile.tests.factories.profile import ProfileFactory
from userprofile.tests.factories.user import UserFactory

from faker import Factory

from utilities import USER_TYPES, MANAGER


faker = Factory.create()


class UserProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = UserFactory()
        profile = ProfileFactory(user=user, project=None)

    def setUp(self):
        self.user = User.objects.last()
        self.profile = Profile.objects.last()

    def test_happy_cases(self):
        # Profiles linked with single user
        profile_count = Profile.objects.filter(user=self.user).count()
        self.assertEqual(profile_count, 1)
        # Choices allowed for Profile Types (designation)
        choices = self.profile._meta.get_field("designation").choices
        self.assertEqual(
            choices,
            USER_TYPES + ((MANAGER, "Manager"),),
        )
        # Adding Project to profile and verifying its added
        project = ProjectFactory()
        project.save()
        self.profile.project = project
        self.profile.save()
        self.assertEqual(self.profile.project.name, project.name)
        # Checking if object name is same as set by str method
        expected_object_name = f"{self.profile.user.username}"
        self.assertEqual(str(self.profile), expected_object_name)
        # Verifying url the is got reverse operation is correct
        self.assertEqual(
            self.profile.get_absolute_url(), f"/users/{self.profile.user.id}"
        )

    def test_no_user_profile(self):
        try:
            ProfileFactory(user=None, project=None)
            self.fail("Profile existing without user")
        except IntegrityError as e:
            pass

    def test_link_mutliple_profiles(self):
        try:
            ProfileFactory(user=self.user, project=None, designation=MANAGER)
            self.fail("Duplicate profile created for same user")
        except Exception as e:
            self.assertEqual(Profile.objects.all().count(), User.objects.all().count())

    def test_custom_designation_for_user(self):
        try:
            self.profile.designation = faker.word(['random', 'words', 'for', 'design', 'ation'])
            self.profile.full_clean()
            self.profile.save()
            self.fail("Random Designation Assigned")
        except ValidationError as e:
            pass
