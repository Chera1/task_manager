from datetime import datetime
from http import HTTPStatus

from main.models import Task, Tag
from main.tests.base import TestViewSetBase


class TestUserTasksViewSet(TestViewSetBase):
    basename = "task_tags"

    def setUp(self) -> None:
        super().setUp()
        self.test_tag = Tag.objects.create(title="test_tag")
        self.task_attributes = {
            "title": "test_task",
            "expired_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "author": self.admin,
            "performer": self.admin,
            "description": "description",
        }

    def test_list(self) -> None:
        task = self.create_task(self.task_attributes)
        task = self.get_expected_task_attr(task)
        tag1 = self.create_tag({"title": "test_tag_1"})
        tag1 = self.get_expected_tag_attr(tag1)
        tag2 = self.create_tag({"title": "test_tag_2"})
        tag2 = self.get_expected_tag_attr(tag2)
        self.add_tags(task, [tag1, tag2])

        tags = self.list(args=[task["id"]])

        assert tags == [tag1, tag2]

    def add_tags(self, task: dict, tags: list) -> None:
        task_instance = Task.objects.get(pk=task["id"])
        task_instance.tags.add(*self.ids(tags))
        task_instance.save()

    def test_retrieve_foreign_tag(self) -> None:
        task = self.create_task(self.task_attributes)
        tag = self.create_tag({"title": "test_tag"})

        response = self.request_retrieve(key=[task.id, tag.id])

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_retrieve(self) -> None:
        task = self.create_task(self.task_attributes)
        created_tag = self.create_tag({"title": "test_tag"})
        created_tag = self.get_expected_tag_attr(created_tag)
        task.tags.add(*self.ids([created_tag]))

        retrieved_tag = self.retrieve(created_tag, key=[task.id, created_tag["id"]])

        assert retrieved_tag == created_tag

    def test_delete(self) -> None:
        task = self.create_task(self.task_attributes)
        created_tag = self.create_tag({"title": "test_tag"})
        created_tag = self.get_expected_tag_attr(created_tag)
        task.tags.add(*self.ids([created_tag]))

        self.delete(key=[task.id, created_tag["id"]])
        retrieved_tag_response = self.request_retrieve(
            created_tag, key=[task.id, created_tag["id"]]
        )

        assert retrieved_tag_response.status_code == HTTPStatus.NOT_FOUND

    def test_update(self) -> None:
        task = self.create_task(self.task_attributes)
        created_tag = self.create_tag({"title": "test_tag"})
        created_tag = self.get_expected_tag_attr(created_tag)
        task.tags.add(*self.ids([created_tag]))

        self.update(
            {
                "title": "new_title",
            },
            key=[task.id, created_tag["id"]],
        )

        retrieved_tag = self.retrieve(created_tag, key=[task.id, created_tag["id"]])

        assert retrieved_tag["title"] == "new_title"
