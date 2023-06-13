from main.test.base import TestViewSetBase
from main.test.fixtures.factories.user import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = dict

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user_attributes = UserFactory.build()
        cls.user_attributes["phone"] = cls.user_attributes["phone"][:20]

    @staticmethod
    def excepted_details(entity: dict, attributes: dict) -> dict:
        del attributes["password"]
        return {**attributes, "id": entity["id"]}

    def test_create(self) -> None:
        user = self.create(self.user_attributes)
        excepted_response = self.excepted_details(user, self.user_attributes)
        assert user == excepted_response

    def test_delete(self) -> None:
        user = self.create(self.user_attributes)
        self.delete(user["id"])

    def test_get(self) -> None:
        created_user = self.create(self.user_attributes)
        retrieved_user = self.retrieve(created_user["id"])
        excepted_response = self.excepted_details(retrieved_user, self.user_attributes)
        assert retrieved_user == excepted_response

    def test_update_last_name(self) -> None:
        user = self.create(self.user_attributes)
        updated_user = self.update(
            {"last_name": "Holms", "username": user["username"]}, user["id"]
        )
        assert updated_user["last_name"] == "Holms"

    def test_list(self) -> None:
        data = self.list()
        assert len(data) == 1

    def test_filters(self) -> None:
        self.create(self.user_attributes)
        users = self.get_filters({"username": "smith"})
        assert len(users) == len(
            [user for user in users if "smith" in user["username"]]
        )
