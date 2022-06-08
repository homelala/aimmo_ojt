import json
import sys

import factory
import pytest
from flask import url_for

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
                print("asdf", logged_in_user)
                return {
                    "email": logged_in_user.email,
                    "name": "test4",
                    "passwd": "test",
                }

            def test_return_400(self, subject):
                assert subject.status_code == 400

    # class Test_login:
