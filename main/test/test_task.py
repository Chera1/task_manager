from datetime import datetime

from main.models import Tag
from main.test.base import TestViewSetBase


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"

    def setUp(self) -> None:
        super().setUp()
        self.test_tag = Tag.objects.create(title="test_tag")
        self.task_attributes = {
            "title": "test_task",
            "expired_date": datetime.now(),
            "author": self.user.id,
            "performer": self.user.id,
            "tags": [self.test_tag.id],
            "description": "description",
        }

    @staticmethod
    def excepted_details(entity: dict, attributes: dict) -> dict:
        return {
            **attributes,
            "id": entity["id"],
            "status": "new_task",
            "expired_date": entity["expired_date"],
        }

    def test_create(self) -> None:
        task = self.create(self.task_attributes)
        excepted_response = self.excepted_details(task, self.task_attributes)
        assert task == excepted_response

    def test_delete(self) -> None:
        task = self.create(self.task_attributes)
        self.delete(task["id"])

    def test_get(self) -> None:
        task = self.create(self.task_attributes)
        task_info = self.retrieve(task["id"])
        excepted_response = self.excepted_details(task_info, self.task_attributes)
        assert task_info == excepted_response

    def test_update_description(self) -> None:
        task = self.create(self.task_attributes)
        updated_task = self.update(
            {
                "description": "new_description",
                "tags": task["tags"],
                "title": task["title"],
            },
            task["id"],
        )
        assert updated_task["description"] == "new_description"

    def test_filters(self) -> None:
        self.create(self.task_attributes)
        tasks = self.get_filters({"status": "new_status"})
        assert len(tasks) == len(
            [user for user in tasks if "new_status" in user["status"]]
        )
