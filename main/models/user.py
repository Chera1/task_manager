from django.db import models
from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory
from faker import Faker
from django.contrib.auth.models import AbstractUser


class TypeRole(models.TextChoices):
    developer = "developer"
    manager = "manager"
    admin = "admin"


class User(AbstractUser):
    role = models.CharField(
        max_length=255, default=TypeRole.developer, choices=TypeRole.choices
    )
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)


class UserFactory(DjangoModelFactory):
    username = Faker().name()
    password = PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User
