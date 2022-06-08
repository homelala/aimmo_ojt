import json
import sys

import factory
import pytest
from flask import url_for
from json import dumps
import traceback
from test.factory.user import UserFactory
import logging

logger = logging.getLogger("test")
sys.path.append(".")

from app.domain import User


class Test_user:
    @pytest.fixture
    def logged_in_user(self):
        return UserFactory.create()

    class Test_signup:
        @pytest.fixture
        def email(self):
            return "test@email.com"

        @pytest.fixture
        def password(self):
            return "abcdefghijk"

        @pytest.fixture
        def name(self):
            return "daniel"

        @pytest.fixture
        def form(self):
            return {
                "email": "test!@daum.com",
                "name": "test4",
                "passwd": "test",
            }

        @pytest.fixture
        def subject(self, client, form):
            # url = url_for("UserView:signup")
            return client.post("/user/signUp", data=json.dumps(form))

        class Test_정상_요청:
            def test_sample(self):
                assert True

            def test_return_200(self, session, subject):
                assert subject.status_code == 200

            def test_user_same_data(self, subject, user_data):
                account = User.objects()[1].account
                assert account == user_data["account"]
