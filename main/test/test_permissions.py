from http import HTTPStatus
import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from main.models import Tag, Task, User


class PermissionTestViewSet(APITestCase):
    url_tasks = reverse("tasks-list")
    url_users = reverse("users-list")
    url_tags = reverse("tags-list")
    client = APIClient()

    def test_not_possible_delete_task_by_authorized_user(self):
        """
        Ensure we can't delete a new task object.
        """
        user = User.objects.create_user("test@test.ru", email=None, password=None)
        self.client.force_login(user)
        content = self.create_task(self.client, user)
        response = self.client.delete(self.url_tasks + str(content["id"]) + "/")
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_not_possible_delete_user_by_authorized_user(self):
        """
        Ensure we can't delete a new user object.
        """
        user = User.objects.create_user("test@test.ru", email=None, password=None)
        self.client.force_login(user)
        response = self.client.delete(self.url_users + str(user.id) + "/")
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_not_possible_delete_tag_by_authorized_user(self):
        """
        Ensure we can't delete a new tag object.
        """
        user = User.objects.create_user("test@test.ru", email=None, password=None)
        tag = self.create_tag(self.client)
        self.client.force_login(user)
        response = self.client.delete(self.url_tags + str(tag["id"]) + "/")
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_not_possible_update_task_by_authorized_user(self):
        """
        Ensure we can't delete a new task object.
        """
        user = User.objects.create_user("test@test.ru", email=None, password=None)
        self.client.force_login(user)
        content = self.create_task(self.client, user)
        response = self.client.put(
            self.url_tasks + str(content["id"]) + "/",
            data={
                "description": "new_description",
                "tags": content["tags"],
                "title": content["title"],
            },
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_not_possible_update_user_by_authorized_user(self):
        """
        Ensure we can't update a new user object.
        """
        user = User.objects.create_user("test@test.ru", email=None, password=None)
        self.client.force_login(user)
        response = self.client.put(
            self.url_users + str(user.id) + "/",
            data={"last_name": "Holms", "username": user.username},
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_not_possible_update_tag_by_authorized_user(self):
        """
        Ensure we can't delete a new tag object.
        """
        user = User.objects.create_user("test@test.ru", email=None, password=None)
        tag = self.create_tag(self.client)
        self.client.force_login(user)
        response = self.client.put(
            self.url_tags + str(tag["id"]) + "/",
            data={
                "title": "test_tag_test",
            },
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_delete_task_by_staff_user(self):
        """
        Ensure we can delete a new task object.
        """
        user = User.objects.create_superuser("test@test.ru", email=None, password=None)
        self.client.force_login(user)
        content = self.create_task(self.client, user)
        response = self.client.delete(self.url_tasks + str(content["id"]) + "/")
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_delete_user_by_staff_user(self):
        """
        Ensure we can delete a new user object.
        """
        user = User.objects.create_superuser("test@test.ru", email=None, password=None)
        self.client.force_login(user)
        response = self.client.delete(self.url_users + str(user.id) + "/")
        assert response.status_code == HTTPStatus.NO_CONTENT

    def create_task(self, client: APIClient, user: User) -> dict:
        """
        Ensure we can create a new task object. If success we return content.
        :param client: client instance
        :param user: logged user
        :return: content of response
        """
        tag_content = self.create_tag(client)
        data = {
            "title": "test_task",
            "expired_date": datetime.datetime.now(),
            "author": user.id,
            "performer": user.id,
            "tags": [tag_content["id"]],
        }
        response = client.post(self.url_tasks, data, format="json")
        content = response.json()
        assert response.status_code == HTTPStatus.CREATED, content
        assert Task.objects.count() == 1
        return content

    def create_tag(self, client: APIClient) -> dict:
        """
        Ensure we can create a new tag object. If success we return content.
        :param client: client instance
        :return: content of response
        """
        url = reverse("tags-list")
        data = {"title": "test_tag"}
        response = client.post(url, data, format="json")
        content = response.json()
        assert response.status_code == HTTPStatus.CREATED, content
        assert Tag.objects.count() == 1
        return content
