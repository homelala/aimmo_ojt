import factory
import pytest
from flask import url_for
from json import dumps

from domain import User
from test.factory.user import UserFactory


class TestUser:
    class Describe_SignUp:
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

        @pytest.fixture
        def subject(self, client, headers, form):
            url = url_for("UserController:signUp")
            return client.post(url, headers=headers, data=dumps(form))

        def test_return_200(self, subject):
            assert subject.status_code == 200

        def test_user_same_data(self, subject, form):
            account = User.objects()[1].account
            assert account == form["account"]
