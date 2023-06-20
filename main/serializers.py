from typing import Any

from rest_framework.exceptions import ValidationError
from celery.result import AsyncResult
from task_manager.tasks import countdown

from task_manager import settings
from .models import User, Task, Tag
from rest_framework import serializers
from django.core.files.base import File
from django.core.validators import FileExtensionValidator


class FileMaxSizeValidator:
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self.max_size:
            raise ValidationError(f"Maximum size {self.max_size} exceeded.")


class UserSerializer(serializers.ModelSerializer):
    avatar_picture = serializers.FileField(
        required=False,
        validators=[
            FileMaxSizeValidator(settings.UPLOAD_MAX_SIZES["avatar_picture"]),
            FileExtensionValidator(["jpeg", "jpg", "png"]),
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "date_of_birth",
            "phone",
            "avatar_picture",
        )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "expired_date",
            "status",
            "author",
            "performer",
            "tags",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title")


class RepresentationSerializer(serializers.Serializer):
    def update(self, instance: Any, validated_data: dict) -> Any:
        pass

    def create(self, validated_data: dict) -> Any:
        pass


class CountDownJobSerializer(RepresentationSerializer):
    seconds = serializers.IntegerField(write_only=True)

    task_id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    def create(self, validated_data: dict) -> AsyncResult:
        return countdown.delay(**validated_data)


class ErrorSerializer(RepresentationSerializer):
    non_field_errors: serializers.ListSerializer = serializers.ListSerializer(
        child=serializers.CharField()
    )


class JobSerializer(RepresentationSerializer):
    task_id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    errors = ErrorSerializer(read_only=True, required=False)
    result = serializers.CharField(required=False)
