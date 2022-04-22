import random
import factory
from faker import Factory
from bugs.models import Bug
from project.models import Project
from userprofile.tests.factories import ProfileFactory
from utilities import NEW, INPROGRESS, COMPLETED, BUG, FEATURE

faker = Factory.create()


class BugFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bug
        django_get_or_create = (
            "project",
            "creator",
            "assigned_to",
        )

    title = faker.sentence()
    description = faker.text()
    deadline = faker.date()
    type = random.choice([BUG, FEATURE])
    status = random.choice([NEW, INPROGRESS, COMPLETED])

    creator = factory.SubFactory(ProfileFactory)
    project = factory.SubFactory(Project)
    assigned_to = factory.SubFactory(ProfileFactory)
    screenshot = None
