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
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
