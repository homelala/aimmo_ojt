import json
from functools import wraps
from flask import request
import jwt

from utils.CustomException import AccessException


def valid_user(f):
    @wraps(f)
    def decorate_user(*args, **kwargs):
        token = json.loads(request.data)["token"]
        if not token:
            raise AccessException("잘못된 접근입니다.")
        try:
            payload = jwt.decode(token, "secret_key", "HS256")
        except jwt.InvalidTokenError:
            raise AccessException("유효하지 않은 토큰입니다.")

        return f(*args, **kwargs)

    return decorate_user
