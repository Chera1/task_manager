from datetime import timedelta
from http import HTTPStatus

from freezegun.api import freeze_time
from requests import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from main.models.user import User
from .fixtures.factories.user import UserFactory


class TestJWTAuth(APITestCase):
    token_url = reverse("token_obtain_pair")
    refresh_token_url = reverse("token_refresh")
    any_api_url = "users"

    @staticmethod
    def create_user() -> dict:
        user_data = UserFactory.build()
        user_data["phone"] = user_data["phone"][:20]
        User.objects.create_user(**user_data)
        return user_data

    def token_request(
        self, username: str = None, password: str = "password"
    ) -> Response:
        client = self.client_class()
        if not username:
            user = self.create_user()
            username = user["username"]
            password = user["password"]
        return client.post(
            self.token_url, data={"username": username, "password": password}
        )

    def refresh_token_request(self, refresh_token: str) -> Response:
        client = self.client_class()
        return client.post(self.refresh_token_url, data={"refresh": refresh_token})

    def get_refresh_token(self) -> str:
        response = self.token_request()
        return response.json()["refresh"]

    def test_successful_auth(self) -> None:
        response = self.token_request()
        assert response.status_code == HTTPStatus.OK
        assert response.json()["refresh"]
        assert response.json()["access"]

    def test_unsuccessful_auth(self) -> None:
        response = self.token_request(username="incorrect_username")
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_refresh_token(self) -> None:
        refresh_token = self.get_refresh_token()
        response = self.refresh_token_request(refresh_token)
        assert response.status_code == HTTPStatus.OK
        assert response.json()["access"]

    def test_refresh_lives_lower_than_one_day(self) -> None:
        with freeze_time() as frozen_time:
            refresh_token = self.get_refresh_token()
            frozen_time.tick(timedelta(hours=23, minutes=59))
            response = self.refresh_token_request(refresh_token)
            assert response.status_code == HTTPStatus.OK
            assert response.json()["access"]

    def test_refresh_dies_after_one_day(self) -> None:
        with freeze_time() as frozen_time:
            refresh_token = self.get_refresh_token()
            frozen_time.tick(timedelta(days=1))
            response = self.refresh_token_request(refresh_token)
            assert response.status_code == HTTPStatus.UNAUTHORIZED
