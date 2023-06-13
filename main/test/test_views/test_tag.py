from main.test.base import TestViewSetBase


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = {"title": "test_tag"}

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {**attributes, "id": entity["id"]}

    def test_create(self) -> None:
        tag = self.create(self.tag_attributes)
        excepted_response = self.expected_details(tag, self.tag_attributes)
        assert tag == excepted_response

    def test_delete(self) -> None:
        tag = self.create(self.tag_attributes)
        self.delete(tag["id"])

    def test_get(self) -> None:
        tag = self.create(self.tag_attributes)
        tag_info = self.retrieve(tag["id"])
        excepted_response = self.expected_details(tag_info, self.tag_attributes)
        assert tag_info == excepted_response

    def test_list(self) -> None:
        tags = [self.create(self.tag_attributes) for _ in range(5)]
        data = self.list()
        assert data == tags
