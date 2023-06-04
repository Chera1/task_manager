from django.db import models
from .user import User
from .tag import Tag


class TypeStatus(models.TextChoices):
    new_task = "new_task"
    in_development = "in_development"
    in_qa = "in_qa"
    in_code_review = "in_code_review"
    ready_for_release = "ready_for_release"
    released = "released"
    archived = "archived"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    expired_date = models.DateTimeField(
        verbose_name="the date by which the task must be completed",
        null=True
    )
    status = models.CharField(
        max_length=255, default=TypeStatus.new_task, choices=TypeStatus.choices
    )
    author = models.ForeignKey(
        User,
        related_name="author",
        on_delete=models.DO_NOTHING,
        verbose_name="author of the task",
        null=True
    )
    performer = models.ForeignKey(
        User,
        related_name="performer",
        on_delete=models.DO_NOTHING,
        verbose_name="performer of the task",
        null=True
    )
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
