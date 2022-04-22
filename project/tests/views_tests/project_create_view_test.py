from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import get_user
from userprofile.models import Profile

from faker import Factory
from django.test import TestCase, Client
from userprofile.tests.factories import UserFactory, ProfileFactory

from utilities import MANAGER


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

    def test_user_authentication(self):
        user = get_user(self.client)
        assert user.is_authenticated

    def test_user_and_profile_match(self):
        self.assertTrue(self.profile.user.username == self.user.username)

    def test_get_response(self):
        response = self.client.get(reverse("add-project"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "add_project.html")
