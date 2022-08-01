from pprint import pprint

import pytest

from test.factory.notice import NoticeFactory
from test.factory.noticeComment import NoticeCommentFactory
from test.factory.user import UserFactory


class Describe_my_page:
    @pytest.fixture
    def logged_in_user(self):
        return UserFactory.create()

    @pytest.fixture
    def register_article(self, logged_in_user):
        return NoticeFactory.create(user=str(logged_in_user.id))

    @pytest.fixture
    def register_comment(self, logged_in_user, register_article):
        return NoticeCommentFactory.create(user=str(logged_in_user.id), notice=str(register_article.id))

    class Context_my_articles:
        @pytest.fixture(scope="function")
        def subject(self, client, headers, register_article):
            url = "/my/" + str(register_article.user.id) + "/articles"
            return client.get(url, headers=headers)

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_data_length(self, subject):
                assert len(subject.json) == 1

            def test_data_value(self, subject, register_article):
                assert subject.json[0]["title"] == register_article.title
                assert subject.json[0]["description"] == register_article.description

    class Context_my_comments:
        @pytest.fixture(scope="function")
        def subject(self, client, headers, register_comment):
            url = "/my/" + str(register_comment.user.id) + "/comments"
            return client.get(url, headers=headers)

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_data_length(self, subject):
                assert len(subject.json) == 1

            def test_data_value(self, subject, register_comment):
                assert subject.json[0]["description"] == register_comment.description
                assert subject.json[0]["notice"]["title"] == register_comment.notice.title