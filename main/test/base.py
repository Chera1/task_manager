from http import HTTPStatus
from typing import Union, List

from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from main.models import User, Tag


class TestViewSetBase(APITestCase):
    admin: User = None
    user: User = None
    client: APIClient = None
    basename: str
    test_tag: Tag

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.admin = cls.create_api_admin()
        cls.user = cls.create_api_user()
        cls.client = APIClient()
        cls.test_tag = Tag.objects.create(**{"title": "test_tag"})

    @classmethod
    def create_api_admin(cls):
        return User.objects.create_superuser("test@test.ru", email=None, password=None)

    @classmethod
    def create_api_user(cls):
        return User.objects.create_user("justuser@test.ru", email=None, password=None)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[int, str]]) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.admin)
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def delete(self, key: Union[int, str]):
        """
        Ensure we can't delete an object by common user and ensure we can delete an object by staff.
        """
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url(key))
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        self.client.logout()
        self.client.force_login(self.admin)
        response = self.client.delete(self.detail_url(key))
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content

    def retrieve(self, key: Union[int, str]):
        self.client.force_login(self.admin)
        response = self.client.get(self.detail_url(key))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def list(self, args: List[Union[str, int]] = None):
        self.client.force_login(self.admin)
        response = self.client.get(self.list_url(args))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, data: dict, key: Union[int, str]):
        """
        Ensure we can't update an object by common user and ensure we can update an object by staff.
        """
        self.client.force_login(self.user)
        response = self.client.put(self.detail_url(key), data=data)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        self.client.logout()
        self.client.force_login(self.admin)
        response = self.client.put(self.detail_url(key), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def get_filters(self, data: dict, args: List[Union[str, int]] = None):
        self.client.force_login(self.user)
        response = self.client.get(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data
