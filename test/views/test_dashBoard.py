import datetime
from pprint import pprint

import pytest

from test.factory.notice import NoticeFactory
from test.factory.noticeComment import NoticeCommentFactory
from test.factory.user import UserFactory


class Describe_DashBoardView:
    @pytest.fixture
    def logged_in_user(self):
        return UserFactory.create()

    @pytest.fixture
    def register_article(self, logged_in_user):
        return NoticeFactory.create(user=str(logged_in_user.id), like=5, register_date=datetime.datetime.now() + datetime.timedelta(days=1))

    @pytest.fixture
    def register_articles(self, logged_in_user):
        return NoticeFactory.create_batch(11, user=str(logged_in_user.id))

    @pytest.fixture
    def register_comment(self, register_article, logged_in_user):
        # print(type(register_article))
        register_article.increase_comment()
        return NoticeCommentFactory.create(notice=str(register_article.id), user=str(logged_in_user.id))

    class Test_top_articles:
        @pytest.fixture(scope="function")
        def category(self):
            return "like"

        @pytest.fixture(scope="function")
        def subject(self, client, register_article, register_articles, register_comment, category, page="1", limit="10"):
            return client.get("/main/top?category=" + category+"&page="+page+"&limit="+limit)

        class Test_상위_좋아요:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_data_length_10(self, subject):
                assert len(subject.json) <= 10

            def test_data_order_by_like(self, subject):
                assert subject.json[0]["like"] > subject.json[1]["like"]

        class Test_최신순:
            @pytest.fixture(scope="function")
            def category(self):
                return "register_date"

            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_data_length_10(self, subject):
                assert len(subject.json) == 10

            def test_data_order_by_recentDay(self, subject):
                assert subject.json[0]["register_date"] > subject.json[1]["register_date"]

        class Test_상위_댓글:
            @pytest.fixture(scope="function")
            def category(self):
                return "count_comments"

            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_data_length_10(self, subject):
                assert len(subject.json) <= 10

            def test_data_order_by_comment(self, subject, register_article):
                assert subject.json[0]["count_comments"] > subject.json[1]["count_comments"]
