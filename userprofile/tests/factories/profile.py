import random
from project.tests.factories import ProjectFactory
from userprofile.models import Profile
import factory
from faker import Factory
from userprofile.tests.factories import UserFactory
from utilities import DEVELOPER, MANAGER, QAENGINEER

faker = Factory.create()


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        django_get_or_create = (
            "user",
            "designation",
            "project",
        )

    user = factory.SubFactory(UserFactory)
    designation = random.choice([MANAGER, DEVELOPER, QAENGINEER])
    project = factory.SubFactory(ProjectFactory)
