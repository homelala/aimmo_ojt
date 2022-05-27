import json
from functools import wraps
from flask import request, jsonify
import jwt


def valid_user(f):
    @wraps(f)
    def decorate_user(*args, **kwargs):
        token = json.loads(request.data)["token"]
        if not token:
            return jsonify({"message": "잘못된 접근입니다."}), 400

        try:
            jwt.decode(token, "secret_key", "HS256")
        except jwt.InvalidTokenError:
            return jsonify({"message": "유요한 토큰이 아닙니다.", "statusCode": 400}), 400

        return f(*args, **kwargs)

    return decorate_user
