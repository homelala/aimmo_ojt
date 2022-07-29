import json

import pytest

from app.domain.notice_comment import NoticeComment
from test.factory.user import UserFactory
from test.factory.notice import NoticeFactory
from app.domain.notice import Notice


class Test_NoticeView:
    @pytest.fixture
    def logged_in_user(self):
        return UserFactory.create()

    @pytest.fixture
    def register_article(self, logged_in_user):
        return NoticeFactory.create(user=logged_in_user.id)

    class Test_post:
        @pytest.fixture
        def form(self, logged_in_user):
            return {
                "title": "test",
                "description": "test to test",
                "tags": ["test1", "test2"],
            }

        @pytest.fixture(scope="function")
        def subject(self, client, headers, form):
            return client.post("/articles/", headers=headers, data=json.dumps(form))

        class Test_정상_요청:
            def test_return_201(self, subject):
                assert subject.status_code == 201

            def test_same_data(self, subject, form):
                assert Notice.objects()[0].title == form["title"]
                assert Notice.objects()[0].description == form["description"]

    class Test_update:
        @pytest.fixture
        def form(self):
            return {
                "title": "updateTitle",
                "description": "update description",
            }

        @pytest.fixture(scope="function")
        def subject(self, client, headers, register_article, form):
            url = "/articles/" + str(register_article.id)
            # form["user"] = register_article.user_id
            return client.put(url, headers=headers, data=json.dumps(form))

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_same_data(self, form, subject):
                assert Notice.objects()[0].title == form["title"]

        class Test_권한이_없는_사용자:
            @pytest.fixture
            def headers(self):
                return {
                    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiamFtZXN3YXR0c0BleGFtcGxlLm5ldCIsIm5hbWUiOiJEYXZpZCBCdXJrZSIsImlkIjoiNjJkZTU4NGY3MDYxMGQ5NzQ5MzdkNjZmIn0.68BSjnDPUjv4zr10PvpihcRDEMVeUgFLwjCEyeko5ik"}

            @pytest.fixture(scope="function")
            def subject(self, client, headers, register_article, form):
                url = "/articles/" + str(register_article.id)
                return client.put(url, headers=headers, data=json.dumps(form))

            def test_return_400(self, form, subject):
                assert subject.status_code == 403
                assert subject.json["message"] == "권한이 없는 게시물입니다."

    class Test_get:
        @pytest.fixture(scope="function")
        def subject(self, client, register_article):
            url = "/articles/" + str(register_article.id)
            return client.get(url)

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_article_length(self, subject):
                assert len(Notice.objects()) == 1

            def test_article_data(self, subject, register_article):
                assert Notice.objects().get()["title"] == register_article.title
                assert Notice.objects().get()["description"] == register_article.description

    class Test_delete:
        @pytest.fixture(scope="function")
        def subject(self, client, headers, register_article):
            url = "/articles/" + str(register_article.id)
            return client.delete(url, headers=headers)

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_article_delete_value(self, subject, register_article):
                assert Notice.objects(id=register_article.id).get()["is_deleted"] == True

    class Test_like:
        @pytest.fixture(scope="function")
        def subject(self, client, headers, register_article):
            url = "/articles/" + str(register_article.id) + "/like"
            return client.get(url, headers=headers)

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_like_count(self, subject, register_article):
                assert Notice.objects(id=register_article.id).get()["like"] == 1

    class Test_comment:
        @pytest.fixture
        def form(self, register_article, logged_in_user):
            return {
                "notice": str(register_article.id),
                "user": str(logged_in_user.id),
                "description": "comment",
            }

        @pytest.fixture(scope="function")
        def subject(self, client, headers, form, register_article):
            url = "/articles/" + str(register_article.id) + "/comment"
            return client.post(url, headers=headers, data=json.dumps(form))

        class Test_정상_요청:
            def test_return_201(self, subject):
                assert subject.status_code == 201

            def test_comment_length(self, subject):
                assert len(NoticeComment.objects()) == 1

            def test_comment_data(self, subject, form):
                assert NoticeComment.objects()[0].description == form["description"]

    class Test_search:
        @pytest.fixture
        def keyword(self, register_article):
            return register_article.title

        @pytest.fixture(scope="function")
        def subject(self, client, headers, keyword):
            url = "/articles" + "/search?title=" + keyword +"&page=1&limit=1"
            return client.get(url, headers=headers)

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_return_data(self, subject, keyword):
                assert subject.json[0]["title"] == keyword

            class Test_부분_검색:
                @pytest.fixture
                def keyword(self, register_article):
                    return register_article.title[0:2]

                def test_return_data(self, subject, keyword):
                    assert subject.json[0]["title"][0:2] == keyword
