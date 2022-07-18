import datetime

import pytest

from app.domain.notice import Notice
from test.factory.notice import NoticeFactory
from test.factory.noticeComment import NoticeCommentFactory
from test.factory.user import UserFactory


class Describe_dashBoard:
    @pytest.fixture
    def logged_in_user(self):
        return UserFactory.create()

    @pytest.fixture
    def register_article(self, logged_in_user):
        return NoticeFactory.create(user_id=str(logged_in_user.id), like=5, register_date=datetime.datetime.now() + datetime.timedelta(days=1))

    @pytest.fixture
    def register_articles(self, logged_in_user):
        return NoticeFactory.create_batch(11, user_id=str(logged_in_user.id))

    @pytest.fixture
    def register_comment(self, register_article, logged_in_user):
        return NoticeCommentFactory.create(notice_id=str(register_article.id), user_id=str(logged_in_user.id))

    class Context_High_like_articles:
        @pytest.fixture(scope="function")
        def subject(self, client, register_article, register_articles):
            return client.get("/main/like")

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_data_length_10(self, subject):
                assert len(subject.json["data"]) <= 10

            def test_data_order_by_like(self, subject):
                assert subject.json["data"][0]["like"] > subject.json["data"][1]["like"]

    class Context_High_comment_articles:
        @pytest.fixture(scope="function")
        def subject(self, client, register_articles, register_comment):
            return client.get("/main/comment")

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_data_length_10(self, subject):
                assert len(subject.json["data"]) <= 10

            def test_data_order_by_comment(self, subject):
                assert len(subject.json["data"][0]["comments"]) > len(subject.json["data"][1]["comments"])

    class Context_Recent_articles:
        @pytest.fixture(scope="function")
        def subject(self, client, register_articles, register_article):
            return client.get("/main/recent/articles")

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_data_length_10(self, subject):
                assert len(subject.json["data"]) == 10

            def test_data_order_by_recentDay(self, subject):
                assert subject.json["data"][0]["register_date"] >= subject.json["data"][1]["register_date"]
