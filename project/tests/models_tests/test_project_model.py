from django.test import TestCase

from project.tests.factories import ProjectFactory
from faker import Factory
from django.db.utils import DataError

faker = Factory.create()

class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = ProjectFactory()

    def test_happy_cases(self):

        # test_profile_object_name
        expected_object_name = f"{self.project.name}"
        self.assertEqual(str(self.project), expected_object_name)

        #test_project_name_length
        project_name_length = self.project._meta.get_field("name").max_length
        self.assertEqual(project_name_length, 50)

        #test_project_name_verbose
        project_name = self.project._meta.get_field("name").verbose_name
        self.assertEqual(project_name, "Project Name")

        #test_project_description_verbose
        project_description = self.project._meta.get_field("description").verbose_name
        self.assertEqual(project_description, "Project Description")

    def test_exceeding_length_project_name(self):
        try:
            self.project.name = faker.sentence(51)
            self.project.save()
            self.fail("Error not raised at project_name max_length")
        except DataError as e:
            pass
