import pytest

from test.factory.notice import NoticeFactory
from test.factory.user import UserFactory


class Describe_my_page:
    @pytest.fixture
    def logged_in_user(self):
        return UserFactory.create()

    @pytest.fixture
    def register_article(self, logged_in_user):
        return NoticeFactory.create(user_id=str(logged_in_user.id))

    class Context_my_articles:
        @pytest.fixture(scope="function")
        def subject(self, client, headers, register_article):
            url = "/my/" + str(register_article.user_id) + "/articles"
            return client.get(url, headers=headers)

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_data_user_id(self, subject):
                assert len(subject.json["data"]) == 1

    class Context_my_comments:
        @pytest.fixture(scope="function")
        def subject(self, client, headers, register_article):
            url = "/my/" + str(register_article.user_id) + "/comments"
            return client.get(url, headers=headers)

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200
