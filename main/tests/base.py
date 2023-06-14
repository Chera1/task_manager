from http import HTTPStatus
from typing import Union, List

from requests import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from main.tests.fixtures.factories.user import UserFactory
from main.models import User, Task, Tag


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
    def create_api_admin(cls) -> User:
        return User.objects.create_superuser("admin", email=None, password=None)

    @classmethod
    def create_api_user(cls) -> User:
        attributes = UserFactory.build()
        return User.objects.create_user(**attributes)

    @classmethod
    def create_task(cls, attributes: dict) -> Task:
        return Task.objects.create(**attributes)

    @classmethod
    def create_tag(cls, attributes: dict) -> Tag:
        return Tag.objects.create(**attributes)

    @classmethod
    def get_expected_task_attr(cls, task: Task) -> dict:
        tag_list = [tag.title for tag in task.tags.all()]
        expected_task_attr = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "expired_date": task.expired_date,
            "performer": task.performer_id,
            "author": task.author_id,
            "tags": tag_list,
            "status": str(task.status),
        }
        return expected_task_attr

    @classmethod
    def get_expected_tag_attr(cls, tag: Tag) -> dict:
        expected_tag_attr = {"id": tag.id, "title": tag.title}
        return expected_tag_attr

    @classmethod
    def detail_url(cls, key: Union[Union[int, str], List[Union[int, str]]]) -> str:
        return reverse(
            f"{cls.basename}-detail", args=key if isinstance(key, list) else [key]
        )

    @classmethod
    def list_url(cls, args: List[Union[int, str]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    @classmethod
    def ids(cls, objects: List[dict]) -> List[int]:
        return [element["id"] for element in objects]

    def request_create(
        self, data: dict, args: List[Union[str, int]] = None
    ) -> Response:
        url = self.list_url(args)
        return self.api_client.post(url, data=data)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> ReturnDict:
        response = self.request_create(data, args)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.json()

    def request_delete(
        self, key: Union[Union[int, str], List[Union[int, str]]] = None
    ) -> Response:
        url = self.detail_url(key)
        return self.api_client.delete(url)

    def delete(self, key: Union[Union[int, str], List[Union[int, str]]]) -> None:
        response = self.request_delete(key)
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content

    def request_retrieve(
        self,
        data: dict = None,
        key: Union[Union[int, str], List[Union[int, str]]] = None,
    ) -> Response:
        url = self.detail_url(key)
        return self.api_client.get(url, data=data)

    def retrieve(
        self, data: dict, key: Union[Union[int, str], List[Union[int, str]]]
    ) -> ReturnDict:
        response = self.request_retrieve(data, key=key)
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

    def request_update(
        self, data: dict, key: Union[Union[int, str], List[Union[int, str]]] = None
    ) -> Response:
        url = self.detail_url(key)
        return self.api_client.put(url, data=data)

    def update(
        self, data: dict, key: Union[Union[int, str], List[Union[int, str]]]
    ) -> ReturnDict:
        response = self.request_update(data, key)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def request_single_resource(self, data: dict = None) -> Response:
        return self.api_client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> ReturnDict:
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def request_patch_single_resource(self, attributes: dict) -> Response:
        url = self.list_url()
        return self.api_client.patch(url, data=attributes)

    def patch_single_resource(self, attributes: dict) -> ReturnDict:
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()
