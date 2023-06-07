from main.test.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
    }

    @staticmethod
    def excepted_details(entity: dict, attributes: dict) -> dict:
        return {**attributes, "id": entity["id"]}

    def test_create(self) -> None:
        user = self.create(self.user_attributes)
        excepted_response = self.excepted_details(user, self.user_attributes)
        assert user == excepted_response

    def test_delete(self) -> None:
        user = self.create(self.user_attributes)
        self.delete(user["id"])

    def test_get(self) -> None:
        user = self.create(self.user_attributes)
        user_info = self.retrieve(user["id"])
        excepted_response = self.excepted_details(user_info, self.user_attributes)
        assert user_info == excepted_response

    def test_update_last_name(self) -> None:
        user = self.create(self.user_attributes)
        updated_user = self.update(
            {"last_name": "Holms", "username": user["username"]}, user["id"]
        )
        assert updated_user["last_name"] == "Holms"

    def test_list(self) -> None:
        data = self.list()
        assert len(data) == 2

    def test_filters(self) -> None:
        self.create(self.user_attributes)
        users = self.get_filters({"username": "smith"})
        assert len(users) == len(
            [user for user in users if "smith" in user["username"]]
        )
