from django.test import TestCase

from project.models import Project


class ProjectTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name="Test Project")

    def test_profile_object_name(self):
        project = Project.objects.get(name="Test Project")
        expected_object_name = f"{project.name}"
        self.assertEqual(str(project), expected_object_name)

    def test_project_name_length(self):
        project = Project.objects.get(name="Test Project")
        project_name_length = project._meta.get_field("name").max_length
        self.assertEqual(project_name_length, 50)

    def test_project_description_length(self):
        project = Project.objects.get(name="Test Project")
        project_name_length = project._meta.get_field("description").max_length
        self.assertEqual(project_name_length, 250)

    def test_project_name_verbose(self):
        project = Project.objects.get(name="Test Project")
        project_name = project._meta.get_field("name").verbose_name
        self.assertEqual(project_name, "Project Name")

    def test_project_description_verbose(self):
        project = Project.objects.get(name="Test Project")
        project_description = project._meta.get_field("description").verbose_name
        self.assertEqual(project_description, "Project Description")
