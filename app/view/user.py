import json
import logging

import jwt
from bson import json_util, ObjectId
from flask import jsonify, request
from marshmallow import fields

from app.domain.user import User

logger = logging.getLogger("test")
from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView
from app.schema.user import UserSignUpSchema, UserLogInSchema, UserUpdateInfoSchema
from app.utils.utils import token_required, marshal_empty, valid_create_user


class UserView(FlaskView):
    route_base = "/user"
    decorators = (doc(tags=["User"]),)

    @route("/", methods=["POST"])
    @doc(tags=["User"], description="User 회원 가입", summary="User 회원 가입")
    @valid_create_user
    @use_kwargs(UserSignUpSchema(), locations=("json",))
    def signup(self, user):
        user_info = user.save()
        return {"user_id": json.loads(json_util.dumps(user_info.id))["$oid"]}, 201

    @route("/log-in", methods=["POST"])
    @doc(description="User 로그인", summary="User 로그인")
    @use_kwargs(UserLogInSchema(), locations=("json",))
    def login(self, user):
        data = json.loads(request.data)
        if not user or not user.check_passwd(data["passwd"]):
            return {"message": "이메일 혹은 비밀번호가 틀렸습니다."}, 405

        payload = {"email": user.email, "name": user.name, "id": str(user.id)}
        token = jwt.encode(payload, "secret_key", algorithm="HS256")
        user.update_token(str(token))
        return {"user_id": json.loads(json_util.dumps(user.id))["$oid"]}, 200

    @route("/", methods=["PUT"])
    @doc(description="User 정보 수정", summary="User 정보 수정")
    @token_required
    @use_kwargs(UserUpdateInfoSchema(), locations=("json",))
    @marshal_empty(code=200)
    def update_info(self, user=None):
        user_info = User.objects(id=ObjectId(user.id)).get()
        user_info.update_name(user.name)

        return "", 200
