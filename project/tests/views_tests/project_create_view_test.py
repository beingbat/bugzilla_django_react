from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import get_user
from userprofile.models import Profile

from faker import Factory
from django.test import TestCase, Client
from userprofile.tests.factories import UserFactory, ProfileFactory

from utilities import MANAGER
from utilities.constants import DEVELOPER


faker = Factory.create()


class ProjectCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = UserFactory()
        ProfileFactory(user=user, designation=MANAGER)

    def setUp(self):
        self.user = User.objects.last()
        self.profile = Profile.objects.last()
        self.client = Client()
        self.client.login(username=self.user.username, password="test")

    def test_happy_cases(self):

        # test_user_authentication
        user = get_user(self.client)
        assert user.is_authenticated

        # test_user_and_profile_match
        self.assertTrue(self.profile.user.username == self.user.username)

        # test_get_response
        response = self.client.get(reverse("add-project"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "add_project.html")

    def test_unauthenticated_user(self):
        self.client.logout()
        try:
            response = self.client.get(reverse("add-project"))
            self.fail("Anonymous User creating Project")
        except TypeError as e:
            pass

    def test_invalid_user(self):
        self.profile.designation = DEVELOPER
        self.profile.save()
        response = self.client.get(reverse("add-project"))
        self.assertTemplateUsed(response, "errors/generic.html")

    def test_title_exceed_limit(self):
        response = self.client.post(
            reverse("add-project"),
            {
                "title": faker.sentence(51),
                "description": faker.text(200),
            },
        )
        self.assertTemplateUsed(response, "add_project.html")


