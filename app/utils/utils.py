from functools import wraps

import jwt
from flask import request, jsonify, g
from flask_apispec import marshal_with
from funcy import partial
from marshmallow import Schema


def valid_user(f):
    @wraps(f)
    def decorate_user(*args, **kwargs):
        token = request.headers["token"]

        try:
            payload = jwt.decode(token, "secret_key", "HS256")
        except jwt.InvalidTokenError:
            return jsonify({"message": "유요한 토큰이 아닙니다."}, 405)
        g.user_id = payload["id"]
        return f(*args, **kwargs)

    return decorate_user


marshal_empty = partial(marshal_with, Schema)
