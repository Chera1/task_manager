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
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        user = self.create(self.user_attributes)
        excepted_response = self.expected_details(user, self.user_attributes)
        assert user == excepted_response

    def test_delete(self):
        user = self.create(self.user_attributes)
        self.delete(user["id"])

    def test_get(self):
        user = self.create(self.user_attributes)
        user_info = self.retrieve(user["id"])
        excepted_response = self.expected_details(user_info, self.user_attributes)
        assert user_info == excepted_response

    def test_update_last_name(self):
        user = self.create(self.user_attributes)
        updated_user = self.update(
            {"last_name": "Holms", "username": user["username"]}, user["id"]
        )
        assert updated_user["last_name"] == "Holms"

    def test_list(self):
        data = self.list()
        assert len(data) == 2

    def test_filters(self):
        self.create(self.user_attributes)
        users = self.get_filters({"username": "smith"})
        assert len(users) == len(
            [user for user in users if "smith" in user["username"]]
        )

    def test_not_possible_update_last_name_by_not_staff_user(self):
        user = self.create(self.user_attributes)
        self.not_possible_update_by_not_staff_user(
            {"last_name": "Holms", "username": user["username"]}, user["id"]
        )

    def test_not_possible_delete_user_by_not_staff_user(self):
        user = self.create(self.user_attributes)
        self.not_possible_delete_by_not_staff_user(user["id"])
