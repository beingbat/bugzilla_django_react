from django.test import TestCase, Client
from project.tests.factories import ProjectFactory
from userprofile.tests.factories import UserFactory, ProfileFactory

from userprofile.models import Profile
from django.contrib.auth.models import User

import random
from faker import Factory

from django.urls import reverse

from utilities import FEATURE, BUG, MANAGER, NEW, QAENGINEER, COMPLETED, INPROGRESS

from django.urls.exceptions import NoReverseMatch

from utilities.constants import DEVELOPER

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

    def test_happy_cases(self):
        # test_get_response_for_bug
        response = self.client.get(
            reverse("add-bug", kwargs={"pk": self.project.id, "slug": BUG})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "add_bug.html")

        # test_get_response_for_feature
        response = self.client.get(
            reverse("add-bug", kwargs={"pk": self.project.id, "slug": FEATURE})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "add_bug.html")

        # test_post_for_bug
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

        # test_post_for_feature
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

    # Catching No reverse error.
    def test_get_response_for_invalid_args(self):
        random_type = faker.word(["random", "words", "for", "bugss", "type"])
        invalid_project = -1
        try:
            response = self.client.get(
            reverse("add-bug", kwargs={"pk": invalid_project, "slug": random_type})
            )
            self.fail("No exception raised on inavlid arguments given to reverse")
        except NoReverseMatch as e:
            pass


    # Catching No reverse error.
    def test_post_response_for_invalid_args(self):
        feature_description = faker.text(200)
        random_type = faker.word(["random", "words", "for", "bugss", "type"])
        invalid_project = -1
        try:
            response = self.client.post(
                reverse("add-bug", kwargs={"pk": invalid_project, "slug": random_type}),
                {
                    "title": faker.sentence(10),
                    "description": feature_description,
                    "status": random.choice([NEW, INPROGRESS, COMPLETED]),
                    "screenshot": "",
                    "assigned_to": "",
                    "deadline": faker.date(),
                },
            )
            self.fail("No exception raised on inavlid arguments given to reverse")
        except NoReverseMatch as e:
            pass


    def test_post_unauthenticated(self):
        self.client.logout()
        feature_description = faker.text(200)
        try:
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
            self.fail("No exception raised on unauthenticated user sending post on bug")
        except TypeError as e:
            pass



    def test_post_invalid_account(self):
        self.profile.designation = DEVELOPER
        self.profile.save()
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
        self.assertTemplateUsed(response, "errors/generic.html")


    def test_post_invalid_title_length(self):
        title = faker.sentence(51)
        response = self.client.post(
            reverse("add-bug", kwargs={"pk": self.project.id, "slug": FEATURE}),
            {
                "title": title,
                "description": faker.text(200),
                "status": random.choice([NEW, INPROGRESS, COMPLETED]),
                "screenshot": "",
                "assigned_to": "",
                "deadline": faker.date(),
            },
        )
        self.assertTemplateUsed(response, "add_bug.html")

    def test_post_invalid_status(self):
        response = self.client.post(
            reverse("add-bug", kwargs={"pk": self.project.id, "slug": FEATURE}),
            {
                "title": faker.text(50),
                "description": faker.text(200),
                "status": faker.text(10),
                "screenshot": "",
                "assigned_to": "",
                "deadline": faker.date(),
            },
        )
        self.assertTemplateUsed(response, "add_bug.html")

    def test_post_no_date(self):
        response = self.client.post(
            reverse("add-bug", kwargs={"pk": self.project.id, "slug": FEATURE}),
            {
                "title": faker.text(50),
                "description": faker.text(200),
                "status": random.choice([NEW, INPROGRESS, COMPLETED]),
                "screenshot": "",
                "assigned_to": "",
                "deadline": "",
            },
        )
        self.assertTemplateUsed(response, "add_bug.html")
