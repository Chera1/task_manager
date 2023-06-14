from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile

from main.tests.base import TestViewSetBase
from main.tests.fixtures.factories.user import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        if attributes.get("password"):
            del attributes["password"]
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": entity["avatar_picture"],
        }

    def test_create(self) -> None:
        user_attributes = UserFactory.build()
        user = self.create(user_attributes)
        excepted_response = self.expected_details(user, user_attributes)
        assert user == excepted_response

    def test_delete(self) -> None:
        user_attributes = UserFactory.build()
        user = self.create(user_attributes)
        self.delete(user["id"])
        undefined_user_response = self.request_retrieve(user, user["id"])
        assert undefined_user_response.status_code == HTTPStatus.NOT_FOUND

    def test_get(self) -> None:
        user_attributes = UserFactory.build()
        created_user = self.create(user_attributes)
        retrieved_user = self.retrieve(created_user, created_user["id"])
        excepted_response = self.expected_details(retrieved_user, user_attributes)
        assert retrieved_user == excepted_response

    def test_update_last_name(self) -> None:
        user_attributes = UserFactory.build()
        user = self.create(user_attributes)
        new_user_attributes = {"last_name": "Holds", "username": user["username"]}
        expected_response = self.expected_details(user, new_user_attributes)
        updated_user = self.update(new_user_attributes, user["id"])
        assert expected_response["last_name"] == updated_user["last_name"]

    def test_list(self) -> None:
        data = self.list()
        assert len(data) == 1

    def test_filters(self) -> None:
        user1_attributes = UserFactory.build()
        user1_attributes["phone"] = user1_attributes["phone"][:20]
        user1 = self.create(data=user1_attributes)
        user2_attributes = UserFactory.build()
        user2_attributes["phone"] = user2_attributes["phone"][:20]
        self.create(data=user2_attributes)

        params = {"last_name": user1["last_name"]}
        response = self.list(params)
        assert [user1] == response

    def test_update_avatar_picture(self) -> None:
        user_attributes = UserFactory.build()
        user = self.create(user_attributes)
        new_user_attributes = UserFactory.build()
        expected_response = self.expected_details(user, new_user_attributes)
        updated_user = self.update(new_user_attributes, user["id"])
        expected_response["avatar_picture"] = updated_user["avatar_picture"]

    def test_large_avatar(self) -> None:
        user_attributes = UserFactory.build(
            avatar_picture=SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024)
        )
        response = self.request_create(user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        user_attributes = UserFactory.build()
        user_attributes["avatar_picture"].name = "bad_extension.pdf"
        response = self.request_create(user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }
