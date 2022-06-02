import sys
import factory
import pytest
from flask import url_for


from json import dumps
import unittest

sys.path.append(".")


from app.domain import User


class TestUser:
    class DescribeSignUp:
        """
        user signUp test
        """

        @pytest.fixture
        def user_data(self):
            return {
                "email": factory.Faker("email").generate(),
                "name": factory.Faker("name").generate(),
                "passwd": factory.Faker("passwd").generate(),
            }

        @pytest.fixture()
        def subject(self, client, headers, user_data):
            url = url_for("UserController:signUp")
            return client.post(url, headers=headers, data=dumps(user_data))

        class Context_정상요청(unittest.TestCase):
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_user_same_data(self, subject, form):
                account = User.objects()[1].account
                assert account == form["account"]
