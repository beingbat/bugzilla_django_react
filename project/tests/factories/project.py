import factory
from faker import Factory
from project.models import Project

faker = Factory.create()


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = faker.text(50)
    description = faker.text(200)
