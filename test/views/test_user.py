import pytest

from test.factory.user import UserFactory


class TestUser:
    @pytest.fixture
    def user_signup(self):
        return UserFactory.create()
