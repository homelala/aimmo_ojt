import jwt
import pytest
from bson.json_util import dumps as bson_dumps
from flask import current_app


@pytest.fixture
def token(logged_in_user):
    if logged_in_user:
        return jwt.encode(
            {"user_id": bson_dumps(logged_in_user.id), "name": logged_in_user.name},
            current_app.config["SECRET"],
            current_app.config["ALGORITHM"],
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
