import json
from functools import wraps
from flask import request, jsonify, g
import jwt
from marshmallow import Schema
from funcy import partial
from flask_apispec import marshal_with
from bson.json_util import loads


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
