from datetime import datetime
from unittest.mock import patch, MagicMock
from django.core import mail
from django.template.loader import render_to_string

from main.models import Task, Tag
from main.services.mail import send_assign_notification
from .base import TestViewSetBase


class TestSendEmail(TestViewSetBase):
    basename = "tasks"

    def setUp(self) -> None:
        super().setUp()
        self.test_tag = Tag.objects.create(title="test_tag")
        self.task_attributes = {
            "title": "test_task",
            "expired_date": datetime.now(),
            "author": self.admin.id,
            "performer": self.admin.id,
            "tags": [self.test_tag.id],
            "description": "description",
        }

    @patch.object(mail, "send_mail")
    def test_send_performer_notification(self, fake_sender: MagicMock) -> None:
        performer = self.admin
        task = self.create(self.task_attributes)
        send_assign_notification(task["id"])

        fake_sender.assert_called_once_with(
            subject="You've assigned a task",
            message="",
            from_email=None,
            recipient_list=[performer.email],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task["id"])},
            ),
        )
