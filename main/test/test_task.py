from datetime import datetime

from main.test.base import TestViewSetBase


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    task_attributes = {
        "title": "test_task",
        "expired_date": datetime.now(),
    }

    @classmethod
    def get_relationship_attributes(cls):
        cls.task_attributes.update(
            **{
                "author": cls.user.id,
                "performer": cls.user.id,
                "tags": [cls.test_tag.id],
                "description": "description",
            }
        )

    @staticmethod
    def excepted_details(entity: dict, attributes: dict):
        return {
            **attributes,
            "id": entity["id"],
            "status": "new_task",
            "expired_date": entity["expired_date"],
        }

    def test_create(self):
        self.get_relationship_attributes()
        task = self.create(self.task_attributes)
        excepted_response = self.excepted_details(task, self.task_attributes)
        assert task == excepted_response

    def test_delete(self):
        self.get_relationship_attributes()
        task = self.create(self.task_attributes)
        self.delete(task["id"])

    def test_get(self):
        self.get_relationship_attributes()
        task = self.create(self.task_attributes)
        task_info = self.retrieve(task["id"])
        excepted_response = self.excepted_details(task_info, self.task_attributes)
        assert task_info == excepted_response

    def test_update_description(self):
        self.get_relationship_attributes()
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

    def test_filters(self):
        self.get_relationship_attributes()
        self.create(self.task_attributes)
        tasks = self.get_filters({"status": "new_status"})
        assert len(tasks) == len(
            [user for user in tasks if "new_status" in user["status"]]
        )
