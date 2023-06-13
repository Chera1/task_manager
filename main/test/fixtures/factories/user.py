from factory import Factory, Faker
from main.models.user import TypeRole
from .base import ImageFileProvider

Faker.add_provider(ImageFileProvider)


class UserFactory(Factory):
    password = Faker("password")
    role = Faker("random_element", elements=TypeRole.values)
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    username = Faker("user_name")
    date_of_birth = Faker("date")
    phone = Faker("phone_number")

    class Meta:
        model = dict
