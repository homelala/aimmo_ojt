import json
import logging

import jwt
from bson import json_util, ObjectId
from flask import jsonify, request

from app.domain.user import User

logger = logging.getLogger("test")
from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView
from app.schema.reponse.ResponseDto import ResponseDto
from app.schema.user import UserSignUpSchema, UserLogInSchema, UserUpdateInfoSchema
from app.schema.reponse.ResponseSchema import ResponseDictSchema
from app.utils.utils import valid_user, marshal_empty, user_create_valid


class UserView(FlaskView):
    route_base = "/user"
    decorators = (doc(tags=["User"]),)

    @route("/", methods=["POST"])
    @doc(tags=["User"], description="User 회원 가입", summary="User 회원 가입")
    @user_create_valid
    @use_kwargs(UserSignUpSchema(), locations=("json",))
    @marshal_with(ResponseDictSchema(), code=200, description="회원 가입 완료")
    def signup(self, user):
        user_info = user.save()
        return ResponseDto({"user_id": json.loads(json_util.dumps(user_info.id))["$oid"]}), 200

    @route("/log-in", methods=["POST"])
    @doc(description="User 로그인", summary="User 로그인")
    @use_kwargs(UserLogInSchema(), locations=("json",))
    @marshal_with(ResponseDictSchema(), code=200, description="로그인 성공")
    def login(self, user):
        data = json.loads(request.data)
        if not user:
            return jsonify({"message": "이메일 혹은 비밀번호가 틀렸습니다."}, 405)
        if not user.check_passwd(data["passwd"]):
            return jsonify({"message": "이메일 혹은 비밀번호가 틀렸습니다."}, 405)

        payload = {"email": user.email, "name": user.name, "id": str(user.id)}
        token = jwt.encode(payload, "secret_key", algorithm="HS256")
        user.update_token(token)

        return ResponseDto({"userId": json.loads(json_util.dumps(user.id))["$oid"]}), 200

    @route("/", methods=["PUT"])
    @doc(description="User 정보 수정", summary="User 정보 수정")
    @valid_user
    @use_kwargs(UserUpdateInfoSchema(), locations=("json",))
    @marshal_empty(code=200)
    def userUpdateInfo(self, user=None):
        user_info = User.objects(id=ObjectId(user.id)).get()
        user_info.update_name(user.name)

        return "", 200
