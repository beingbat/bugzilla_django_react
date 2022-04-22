from django.test import TestCase

from project.tests.factories import ProjectFactory


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = ProjectFactory()

    def test_profile_object_name(self):
        expected_object_name = f"{self.project.name}"
        self.assertEqual(str(self.project), expected_object_name)

    def test_project_name_length(self):
        project_name_length = self.project._meta.get_field("name").max_length
        self.assertEqual(project_name_length, 50)

    def test_project_description_length(self):
        project_name_length = self.project._meta.get_field("description").max_length
        self.assertEqual(project_name_length, 250)

    def test_project_name_verbose(self):
        project_name = self.project._meta.get_field("name").verbose_name
        self.assertEqual(project_name, "Project Name")

    def test_project_description_verbose(self):
        project_description = self.project._meta.get_field("description").verbose_name
        self.assertEqual(project_description, "Project Description")
