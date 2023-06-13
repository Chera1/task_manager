from http import HTTPStatus
from typing import Union, List

from requests import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from main.models import User


class TestViewSetBase(APITestCase):
    admin: User = None
    api_client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.admin = cls.create_api_admin()
        cls.api_client = APIClient()
        cls.api_client.force_login(cls.admin)

    @classmethod
    def create_api_admin(cls):
        return User.objects.create_superuser("test@test.ru", email=None, password=None)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[int, str]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def request_create(
        self, data: dict, args: List[Union[str, int]] = None
    ) -> Response:
        url = self.list_url(args)
        return self.api_client.post(url, data=data)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> ReturnDict:
        response = self.request_create(data, args)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.json()

    def request_delete(self, key: Union[int, str] = None) -> Response:
        url = self.detail_url(key)
        return self.api_client.delete(url)

    def delete(self, key: Union[int, str]) -> None:
        response = self.request_delete(key)
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content

    def request_retrieve(
        self, data: dict = None, key: Union[int, str] = None
    ) -> Response:
        url = self.detail_url(key)
        return self.api_client.get(url, data=data)

    def retrieve(self, key: Union[int, str]) -> ReturnDict:
        response = self.request_retrieve(key=key)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def request_list(
        self, data: dict = None, args: List[Union[str, int]] = None
    ) -> Response:
        url = self.list_url(args)
        return self.api_client.get(url, data=data)

    def list(self, data: dict = None, args: List[Union[str, int]] = None) -> ReturnList:
        response = self.request_list(data, args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def request_update(self, data: dict, key: Union[int, str] = None) -> Response:
        url = self.detail_url(key)
        return self.api_client.put(url, data=data)

    def update(self, data: dict, key: Union[int, str]) -> ReturnDict:
        response = self.request_update(data, key)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()
