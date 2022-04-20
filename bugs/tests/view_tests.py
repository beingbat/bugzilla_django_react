from django.utils.timezone import now
from django.test import TestCase, Client
from django.urls import reverse
from project.models import Project
from userprofile.models import Profile
from django.contrib.auth.models import User

from utilities import FEATURE, BUG, MANAGER, NEW


class TestBugAddView(TestCase):
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
        self.project = Project.objects.create(name="Test Project")

    def test_get_response_for_bug(self):
        response = self.client.get(
            reverse("add-bug", kwargs={"pk": self.project.id, "slug": BUG})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "add_bug.html")

    def test_get_response_for_feature(self):
        response = self.client.get(
            reverse("add-bug", kwargs={"pk": self.project.id, "slug": FEATURE})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "add_bug.html")

    def test_post_for_bug(self):
        response = self.client.post(
            f"/bugs/add/{self.project.id}/bug",
            {
                "title": "Bug Title Test",
                "description": "Bug Test Description",
                "status": NEW,
                "screenshot": "",
                "assigned_to": "",
                "deadline": now,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Bug Test Description" in response.content)

    def test_post_for_feature(self):
        response = self.client.post(
            f"/bugs/add/{self.project.id}/feature",
            {
                "title": "Feature Title Test",
                "description": "Feature Test Description",
                "status": NEW,
                "screenshot": "",
                "assigned_to": "",
                "deadline": now,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Feature Test Description" in response.content)
