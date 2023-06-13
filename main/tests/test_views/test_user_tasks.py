from datetime import datetime
from http import HTTPStatus


from main.tests.base import TestViewSetBase


class TestUserTasksViewSet(TestViewSetBase):
    basename = "user_tasks"

    def setUp(self) -> None:
        super().setUp()
        self.task_attributes = {
            "title": "test_task",
            "expired_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "author": self.admin,
            "performer": self.admin,
            "description": "description",
        }

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {
            **attributes,
            "id": entity["id"],
            "expired_date": entity["expired_date"],
        }

    def test_list(self) -> None:
        user = self.admin
        task1 = self.create_task(self.task_attributes)
        task1 = self.get_expected_task_attr(task1)
        tasks = self.list(args=[user.id])
        assert tasks == [task1]

    def test_retrieve_foreign_task(self) -> None:
        second_user = self.create_api_user()
        task = self.create_task(self.task_attributes)

        response = self.request_retrieve(key=[second_user.id, task.id])

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_retrieve(self) -> None:
        user = self.admin
        created_task = self.create_task(self.task_attributes)
        created_task = self.get_expected_task_attr(created_task)

        retrieved_task = self.retrieve(created_task, key=[user.id, created_task["id"]])

        assert retrieved_task == created_task
