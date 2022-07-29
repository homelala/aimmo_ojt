import json
from functools import wraps
from flask import request, jsonify, g

import jwt
from bson import ObjectId
from flask_apispec import marshal_with
from funcy import partial
from marshmallow import Schema
from mongoengine import DoesNotExist

from app.domain.notice import Notice
from app.domain.user import User


def token_required(f):
    @wraps(f)
    def decorate_user(*args, **kwargs):
        token = request.headers["token"]
        print(token)
        try:
            payload = jwt.decode(token, "secret_key", "HS256")
        except jwt.InvalidTokenError:
            return jsonify({"message": "유요한 토큰이 아닙니다."}), 403
        g.user_id = payload["id"]
        return f(*args, **kwargs)

    return decorate_user


def valid_create_user(f):
    @wraps(f)
    def decorate_user(*args, **kwargs):
        data = json.loads(request.data)
        already_user = User.objects(email=data["email"])
        if already_user:
            return jsonify({"message": "이미 존재하는 계정입니다."}), 400
        return f(*args, **kwargs)

    return decorate_user


def valid_article_user(f):
    @wraps(f)
    def decorate_article(*args, **kwargs):
        article = Notice.objects(id=ObjectId(kwargs["article_id"])).get()
        if str(article.user.id) != g.user_id:
            return jsonify({"message": "권한이 없는 게시물입니다."}), 403
        return f(*args, **kwargs)

    return decorate_article


def valid_article(f):
    @wraps(f)
    def decorate_article(*args, **kwargs):
        try:
            article = Notice.objects(id=ObjectId(kwargs["article_id"])).get()
            if article["is_deleted"]:
                return jsonify({"message": "존재하지 않는 게시물입니다."}), 404
        except DoesNotExist:
            return jsonify({"message": "존재하지 않는 게시물입니다."}), 404

        return f(*args, **kwargs)

    return decorate_article


marshal_empty = partial(marshal_with, Schema)
