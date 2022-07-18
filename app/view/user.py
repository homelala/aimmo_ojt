import json
import logging

from bson import json_util

logger = logging.getLogger("test")
from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView
from app.schema.reponse.ResponseDto import ResponseDto
from app.schema.user import UserSignUpSchema, UserLogInSchema, UserUpdateInfoSchema
from app.schema.error.ApiErrorSchema import ApiErrorSchema
from app.schema.reponse.ResponseSchema import ResponseDictSchema
from app.service import userService
from app.utils.CustomException import CustomException
from app.utils.ErrorResponseDto import ErrorResponseDto
from app.utils.utils import valid_user, marshal_empty


class UserView(FlaskView):
    route_base = "/user"
    decorators = (doc(tags=["User"]),)

    @route("/", methods=["POST"])
    @doc(tags=["User"], description="User 회원 가입", summary="User 회원 가입")
    @use_kwargs(UserSignUpSchema(), locations=("json",))
    @marshal_with(ResponseDictSchema(), code=200, description="회원 가입 완료")
    @marshal_with(ApiErrorSchema(), code=402, description="회원 가입 실패")
    def signup(self, user):
        try:
            user_info = userService.userSignUp(user)
            return ResponseDto({"user_id": json.loads(json_util.dumps(user_info.id))["$oid"]}), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), e.statusCode

    @route("/logIn", methods=["POST"])
    @doc(description="User 로그인", summary="User 로그인")
    @use_kwargs(UserLogInSchema(), locations=("json",))
    @marshal_with(ResponseDictSchema(), code=200, description="로그인 성공")
    @marshal_with(ApiErrorSchema(), code=401, description="로그인 실패")
    def login(self, user):
        try:
            user_info = userService.userLogIn(user, user["passwd"])
            return ResponseDto({"userId": json.loads(json_util.dumps(user_info.id))["$oid"]}), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), e.statusCode

    @route("/", methods=["PUT"])
    @doc(description="User 정보 수정", summary="User 정보 수정")
    @valid_user
    @use_kwargs(UserUpdateInfoSchema(), locations=("json",))
    @marshal_empty(code=200)
    @marshal_with(ApiErrorSchema(), code=403, description="정보 수정 실패")
    def userUpdateInfo(self, user=None):
        try:
            userService.userUpdateInfo(user)
            return "", 200
        except CustomException as e:
            return ErrorResponseDto(e.message), e.statusCode
