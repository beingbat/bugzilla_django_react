from django.test import TestCase, Client

from django.utils.timezone import now
from django.urls import reverse

from project.models import Project
from userprofile.models import Profile
from django.contrib.auth.models import User

from utilities import FEATURE, BUG, MANAGER, NEW


class ProjectCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testUser",
            password="testPassword",
        )
        self.profile = Profile.objects.create(
            user=self.user, designation=MANAGER, project=None
        )
        self.client = Client()
        self.client.login(username="testUser", password="testPassword")

    def test_get_response(self):
        response = self.client.get(reverse("add-project"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "add_project.html")

    def test_post(self):
        response = self.client.post(
            f"/project/add/",
            {
                "name": "Project Title Test",
                "description": "Project Test Description",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Project Test Description" in response.content)
