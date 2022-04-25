from django.test import TestCase

from django.core.validators import FileExtensionValidator
from django.db.utils import DataError, IntegrityError
from django.core.exceptions import ValidationError

from bugs.models import Bug
from project.models import Project

from project.tests.factories import ProjectFactory
from userprofile.tests.factories import UserFactory, ProfileFactory
from bugs.tests.factories import BugFactory

from utilities import BUG_TYPE, BUG_STATUS, QAENGINEER, DEVELOPER, MANAGER

import random

from faker import Factory

faker = Factory.create()


class BugTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        project = ProjectFactory()
        user = UserFactory()
        profile = ProfileFactory(
            user=user, designation=random.choice([MANAGER, QAENGINEER])
        )
        BugFactory(creator=profile, project=project, assigned_to=None)

    def setUp(self):
        self.bug = Bug.objects.last()
        self.project = Project.objects.last()

    def test_happy_cases(self):

        # test_bug_linked_project_name
        self.assertEqual(self.bug.project.name, self.project.name)

        # test_expected_object_name
        expected_object_name = f"{self.bug.title}"
        self.assertEqual(str(self.bug), expected_object_name)

        # test_absolute_url
        self.assertEqual(self.bug.get_absolute_url(), f"/bugs/{self.bug.uuid}")

        # test_unique_together_constraint
        unique_together = self.bug._meta.unique_together
        self.assertEquals(unique_together[0], ("project", "title"))

        # test_bug_type_choices
        choices = self.bug._meta.get_field("type").choices
        self.assertEqual(choices, BUG_TYPE)

        # test_bug_status_choices
        choices = self.bug._meta.get_field("status").choices
        self.assertEqual(choices, BUG_STATUS)

        # test_creator_limit_choices
        choices = self.bug._meta.get_field("creator").get_limit_choices_to()
        self.assertEqual(choices, {"designation": QAENGINEER})

        # test_assigned_to_limit_choices
        choices = self.bug._meta.get_field("assigned_to").get_limit_choices_to()
        self.assertEqual(choices, {"designation": DEVELOPER})

        # test_screenshot_file_extension_validations
        choices = self.bug._meta.get_field("screenshot").validators[0]
        self.assertEqual(
            choices.message, FileExtensionValidator(["png", "gif"]).message
        )

    def test_bug_without_project(self):
        try:
            BugFactory(creator=self.bug.creator, project=None, assigned_to=None)
            self.fail("Bug creation without project")
        except IntegrityError as e:
            pass

    def test_bug_title_max_length_exceed(self):
        try:
            self.bug.title = faker.sentence(51)
            self.bug.save()
            self.fail("Error not raised at bug title max_length exceed")
        except DataError as e:
            pass

    def test_random_value_for_type(self):
        try:
            self.bug.type = faker.word(["random", "words", "for", "bugss", "type"])
            self.bug.full_clean()
            self.bug.save()
            self.fail("Random Bug Type Assigned")
        except ValidationError as e:
            pass

    def test_random_value_for_status(self):
        try:
            self.bug.status = faker.word(["random", "words", "for", "bug", "status"])
            self.bug.full_clean()
            self.bug.save()
            self.fail("Random Status Assigned to bug/feature")
        except ValidationError as e:
            pass

    def test_bug_without_creator(self):
        try:
            BugFactory(creator=None, project=self.project)
            self.fail("Bug existing without Creator")
        except IntegrityError as e:
            pass

    def test_bug_with_duplicate_name_in_same_project(self):
        try:
            Bug.objects.create(creator=self.bug.creator, project=self.bug.project, title=self.bug.title)
            print(Bug.objects.all())
            self.fail("Bug existing with dupicate name in same project")
        except IntegrityError as e:
            pass

    def test_bug_without_status(self):
        try:
            BugFactory(creator=self.bug.creator, project=self.bug.project, status=None)
            self.fail("Bug/feature existing without bug/feature status (not null constrained violated)")
        except IntegrityError as e:
            pass

    def test_bug_without_type(self):
        try:
            BugFactory(creator=self.bug.creator, project=self.bug.project, type=None)
            self.fail("Bug existing without bug type (not null constrained violated)")
        except IntegrityError as e:
            pass
