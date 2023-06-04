from django.db import models

from django.contrib.auth.models import AbstractUser


class TypeRole(models.TextChoices):
    developer = "developer"
    manager = "manager"
    admin = "admin"


class User(AbstractUser):
    role = models.CharField(
        max_length=255, default=TypeRole.developer, choices=TypeRole.choices
    )
