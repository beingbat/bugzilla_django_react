from django.test import TestCase

from bugs.models import Bug
from project.models import Project

from project.tests.factories import ProjectFactory
from userprofile.tests.factories import UserFactory, ProfileFactory
from bugs.tests.factories import BugFactory

from utilities import BUG_TYPE, BUG_STATUS, QAENGINEER, DEVELOPER, MANAGER

import random

from django.core.validators import FileExtensionValidator

class BugTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        project = ProjectFactory()
        user = UserFactory()
        profile = ProfileFactory(user=user, designation=random.choice([MANAGER, QAENGINEER]))
        BugFactory(creator=profile, project=project, assigned_to=None)

    def setUp(self):
        self.bug = Bug.objects.last()
        self.project = Project.objects.last()

    def test_bug_linked_project_name(self):
        self.assertEqual(self.bug.project.name, self.project.name)

    def test_expected_object_name(self):
        expected_object_name = f"{self.bug.title}"
        self.assertEqual(str(self.bug), expected_object_name)

    def test_absolute_url(self):
        self.assertEqual(self.bug.get_absolute_url(), f"/bugs/{self.bug.uuid}")

    def test_unique_together_constraint(self):
        unique_together = self.bug._meta.unique_together
        self.assertEquals(unique_together[0], ("project", "title"))

    def test_bug_type_choices(self):
        choices = self.bug._meta.get_field("type").choices
        self.assertEqual(choices, BUG_TYPE)

    def test_bug_status_choices(self):
        choices = self.bug._meta.get_field("status").choices
        self.assertEqual(choices, BUG_STATUS)

    def test_creator_limit_choices(self):
        choices = self.bug._meta.get_field("creator").get_limit_choices_to()
        self.assertEqual(choices, {"designation": QAENGINEER})

    def test_assigned_to_limit_choices(self):
        choices = self.bug._meta.get_field("assigned_to").get_limit_choices_to()
        self.assertEqual(choices, {"designation": DEVELOPER})


    def test_screenshot_file_extension_validations(self):
        choices = self.bug._meta.get_field("screenshot").validators[0]
        self.assertEqual(
            choices.message, FileExtensionValidator(["png", "gif"]).message
        )
