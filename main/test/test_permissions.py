from http import HTTPStatus
from typing import Type, Container
import json
import datetime

from django.db import models
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from main.models import Tag, Task, User


class AccountTests(APITestCase):
    def test_delete_task_by_authorized_user(self):
        """
        Ensure we can't delete a new task object.
        """
        url = reverse('tasks-list')
        self.client = APIClient()
        user = User.objects.create_user("test@test.ru", email=None, password=None)
        self.client.force_login(user)
        content = self.create_task(self.client, user)
        response = self.client.delete(url + str(content["id"]) + "/")
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_task_by_staff_user(self):
        """
        Ensure we can delete a new task object.
        """
        url = reverse('tasks-list')
        self.client = APIClient()
        user = User.objects.create_superuser("test@test.ru", email=None, password=None)
        self.client.force_login(user)
        content = self.create_task(self.client, user)
        response = self.client.delete(url + str(content["id"]) + "/")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def create_task(self, client, user):
        """
        Ensure we can create a new task object. If success we return content.
        :param client: client instance
        :param user: logged user
        :return: content of response
        """
        tag_content = self.create_tag(client)
        url = reverse('tasks-list')
        data = {"title": "test_task", "expired_date": datetime.datetime.now(), "author": user.id, "performer": user.id,
                "tags": [tag_content["id"]]}
        response = client.post(url, data, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, HTTPStatus.CREATED, content)
        self.assertEqual(Task.objects.count(), 1)
        return content

    def create_tag(self, client):
        """
        Ensure we can create a new tag object. If success we return content.
        :param client: client instance
        :return: content of response
        """
        url = reverse('tags-list')
        data = {"title": "test_tag"}
        response = client.post(url, data, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, HTTPStatus.CREATED, content)
        self.assertEqual(Tag.objects.count(), 1)
        return content
