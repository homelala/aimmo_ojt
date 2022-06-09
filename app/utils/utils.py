import json
from functools import wraps
from flask import request, jsonify
import jwt


def valid_user(f):
    @wraps(f)
    def decorate_user(*args, **kwargs):
        token = request.headers["token"]

        try:
            jwt.decode(token, "secret_key", "HS256")
        except jwt.InvalidTokenError:
            return jsonify({"message": "유요한 토큰이 아닙니다.", "statusCode": 400}), 400

        return f(*args, **kwargs)

    return decorate_user
