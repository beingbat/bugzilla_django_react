from enum import unique
from django.test import TestCase

from django.core.validators import FileExtensionValidator

from django.contrib.auth.models import User
from bugs.models import Bug
from project.models import Project
from userprofile.models import Profile
from utilities import BUG_TYPE, BUG_STATUS, QAENGINEER, DEVELOPER


class BugTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        project = Project.objects.create(name="Test Project")
        user = User.objects.create(
            first_name="Big", last_name="Bob", username="bug_user"
        )
        profile = Profile.objects.create(user=user)
        Bug.objects.create(
            creator=profile,
            project=project,
            title="Test Bug",
        )

    def test_bug_linked_project_name(self):
        project = Project.objects.get(id=1)
        bug = Bug.objects.get(project=project)
        self.assertEqual(bug.project.name, "Test Project")

    def test_expected_object_name(self):
        bug = Bug.objects.get(project_id=1)
        expected_object_name = f"{bug.title}"
        self.assertEqual(str(bug), expected_object_name)

    def test_absolute_url(self):
        bug = Bug.objects.get(project_id=1)
        self.assertEqual(bug.get_absolute_url(), f"/bugs/{bug.uuid}")

    def test_unique_together_constraint(self):
        bug = Bug.objects.get(project_id=1)
        unique_together = bug._meta.unique_together
        self.assertEquals(unique_together[0], ("project", "title"))

    def test_bug_type_choices(self):
        bug = Bug.objects.get(project_id=1)
        choices = bug._meta.get_field("type").choices
        self.assertEqual(choices, BUG_TYPE)

    def test_bug_status_choices(self):
        bug = Bug.objects.get(project_id=1)
        choices = bug._meta.get_field("status").choices
        self.assertEqual(choices, BUG_STATUS)

    def test_creator_limit_choices(self):
        bug = Bug.objects.get(project_id=1)
        choices = bug._meta.get_field("creator").get_limit_choices_to()
        self.assertEqual(choices, {"designation": QAENGINEER})

    def test_assigned_to_limit_choices(self):
        bug = Bug.objects.get(project_id=1)
        choices = bug._meta.get_field("assigned_to").get_limit_choices_to()
        self.assertEqual(choices, {"designation": DEVELOPER})
        pass

    def test_deadline_date(self):
        pass

    def test_screenshot_file_extension_validations(self):
        bug = Bug.objects.get(project_id=1)
        choices = bug._meta.get_field("screenshot").validators[0]
        self.assertEqual(
            choices.message, FileExtensionValidator(["png", "gif"]).message
        )
