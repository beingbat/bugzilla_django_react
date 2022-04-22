from django.test import TestCase, Client
from project.tests.factories import ProjectFactory
from userprofile.tests.factories import UserFactory, ProfileFactory

from userprofile.models import Profile
from django.contrib.auth.models import User

import random
from faker import Factory

from django.urls import reverse

from utilities import FEATURE, BUG, MANAGER, NEW, QAENGINEER, COMPLETED, INPROGRESS

faker = Factory.create()


class TestBugAddView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = UserFactory()
        ProfileFactory(user=user, designation=random.choice([MANAGER, QAENGINEER]))

    def setUp(self):
        self.user = User.objects.last()
        self.profile = Profile.objects.last()
        self.client = Client()
        self.client.login(username=self.user.username, password="test")
        self.project = ProjectFactory()

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
        bug_description = faker.text(200)
        response = self.client.post(
            reverse("add-bug", kwargs={"pk": self.project.id, "slug": BUG}),
            {
                "title": faker.sentence(10),
                "description": bug_description,
                "status": random.choice([NEW, INPROGRESS, COMPLETED]),
                "screenshot": "",
                "assigned_to": "",
                "deadline": faker.date(),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(bytes(bug_description, "utf-8") in response.content)

    def test_post_for_feature(self):
        feature_description = faker.text(200)
        response = self.client.post(
            reverse("add-bug", kwargs={"pk": self.project.id, "slug": FEATURE}),
            {
                "title": faker.sentence(10),
                "description": feature_description,
                "status": random.choice([NEW, INPROGRESS, COMPLETED]),
                "screenshot": "",
                "assigned_to": "",
                "deadline": faker.date(),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(bytes(feature_description, "utf-8") in response.content)
