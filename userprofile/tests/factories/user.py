import factory
from django.contrib.auth import get_user_model
from faker import Factory

faker = Factory.create()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = faker.first_name()
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()
    password = factory.PostGenerationMethodCall("set_password", "test")
