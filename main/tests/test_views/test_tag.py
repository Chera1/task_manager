from http import HTTPStatus

from main.tests.base import TestViewSetBase


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
        undefined_tag_response = self.request_retrieve(tag, tag["id"])
        assert undefined_tag_response.status_code == HTTPStatus.NOT_FOUND

    def test_get(self) -> None:
        tag = self.create(self.tag_attributes)
        tag_info = self.retrieve(tag, tag["id"])
        excepted_response = self.expected_details(tag_info, self.tag_attributes)
        assert tag_info == excepted_response

    def test_list(self) -> None:
        tags = [self.create(self.tag_attributes) for _ in range(5)]
        data = self.list()
        assert data == tags

    def test_update(self) -> None:
        tag = self.create(self.tag_attributes)
        new_tag_attributes = {"title": "new_title"}
        expected_response = self.expected_details(tag, new_tag_attributes)
        updated_tag = self.update(new_tag_attributes, tag["id"])
        assert expected_response["title"] == updated_tag["title"]
