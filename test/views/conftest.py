import jwt
import pytest
from flask import current_app


@pytest.fixture
def token(logged_in_user):
    if logged_in_user:
        return jwt.encode(
            {"user_id": logged_in_user.email, "name": logged_in_user.name, "id": str(logged_in_user.id)},
            "secret_key",
            algorithm="HS256",
        )
    else:
        return None


@pytest.fixture
def headers(token):
    if token:
        headers = {"token": token}
    else:
        headers = None
    return headers
