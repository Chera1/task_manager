from django.db import models
from django.contrib.auth.models import AbstractUser
from main.services.storage_backends import public_storage


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
    avatar_picture = models.ImageField(null=True, storage=public_storage)
