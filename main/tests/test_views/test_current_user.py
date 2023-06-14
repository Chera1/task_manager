from main.tests.base import TestViewSetBase


class TestCurrentUserViewSet(TestViewSetBase):
    basename = "current_user"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def test_retrieve(self):
        user = self.single_resource()

        assert user == {
            "id": self.admin.id,
            "email": self.admin.email,
            "first_name": self.admin.first_name,
            "last_name": self.admin.last_name,
            "role": self.admin.role,
            "username": self.admin.username,
            "phone": self.admin.phone,
            "date_of_birth": self.admin.date_of_birth,
            "avatar_picture": self.admin.avatar_picture,
        }

    def test_patch(self):
        self.patch_single_resource(
            {"first_name": "TestName", "username": self.admin.username}
        )

        user = self.single_resource()
        assert user["first_name"] == "TestName"
