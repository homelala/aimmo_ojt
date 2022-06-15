import json
import sys

import pytest

from test.factory.user import UserFactory
import logging
from app.domain.User import User

logger = logging.getLogger("test")
sys.path.append(".")


class Test_user:
    @pytest.fixture
    def logged_in_user(self):
        return UserFactory.create()

    class Test_signup:
        @pytest.fixture
        def form(self):
            return {
                "email": "test!@daum.com",
                "name": "test4",
                "passwd": "test",
            }

        @pytest.fixture(scope="function")
        def subject(self, client, form):
            # url = url_for("UserView:signup")
            return client.post("/user/signUp", data=json.dumps(form))

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_user_갯수가_증가한다(self, subject):
                total_user_count = User.objects().count()
                assert total_user_count == 1

            def test_user_same_data(self, subject, form):
                account = User.objects()[0].email
                assert account == form["email"]

        class Test_중복_계정:
            @pytest.fixture
            def form(self, logged_in_user):
                return {
                    "email": logged_in_user.email,
                    "name": "test4",
                    "passwd": "test",
                }

            def test_return_400(self, subject):
                assert subject.status_code == 402

    class Test_login:
        @pytest.fixture
        def signup_user(self):
            return UserFactory.create(email="test@naver.com", passwd="1111", name="test")

        @pytest.fixture
        def form(self):
            return {
                "email": "test@naver.com",
                "passwd": "1111",
            }

        @pytest.fixture(scope="function")
        def subject(self, client, signup_user, form):
            return client.post("/user/logIn", data=json.dumps(form))

        class Test_정상_요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

        class Test_이메일이_틀렸을경우:
            @pytest.fixture
            def form(self):
                return {
                    "email": "fail@naver.com",
                    "passwd": "1111",
                }

            def test_return_400(self, subject):
                assert subject.status_code == 401
                assert subject.json["message"] == "이메일 혹은 비밀번호가 틀렸습니다."

        class Test_비밀번호가_틀렸을경우:
            @pytest.fixture
            def form(self):
                return {
                    "email": "test@naver.com",
                    "passwd": "2222",
                }

            def test_return_400(self, subject):
                assert subject.status_code == 401
                assert subject.json["message"] == "이메일 혹은 비밀번호가 틀렸습니다."

    class Test_update:
        @pytest.fixture
        def form(self, logged_in_user):
            return {
                "id": str(logged_in_user.id),
                "name": "updateName",
            }

        @pytest.fixture(scope="function")
        def subject(self, client, headers, form):
            return client.put("/user/", headers=headers, data=json.dumps(form))

        class Test_정상_처리:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_same_data(self, subject, form):
                name = User.objects()[0].name
                assert name == form["name"]

        class Test_토근_인증_실패:
            @pytest.fixture
            def headers(self):
                return {"token": "test_fail"}

            def test_유효하지_않은_토큰(self, subject):
                assert subject.json["message"] == "유요한 토큰이 아닙니다."
                assert subject.status_code == 405
