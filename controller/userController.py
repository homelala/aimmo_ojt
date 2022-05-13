from bson import json_util
from flask import request
import json
from flask_apispec import use_kwargs
from flask_classful import route, FlaskView
from dto.ResponseDto import ResponseDto
from dto.UserCreateDto import UserCreateDto
from dto.UserLogInDto import UserLogInDto
from dto.UserUpdateInfoDto import UserUpdateInfoDto
from schema.UserSchema import UserSchema
from service import userService
from utils.CustomException import CustomException
from utils.ErrorResponseDto import ErrorResponseDto


class UserController(FlaskView):
    route_base = "/user"

    @route("/signUp", methods=["POST"])
    @use_kwargs(UserSchema(), locations=("json",))
    def userSignUP(self, user=None):
        try:
            userId = userService.userSignUp(user)
            return ResponseDto(200, "회원 가입 완료", {"userId": json.loads(json_util.dumps(userId))["$oid"]}).toJSON(), 200
        except CustomException as e:
            return ErrorResponseDto(e.message, e.statusCode).toJSON()

    @route("/logIn", methods=["POST"])
    def userLogIn(self):
        try:
            body = request.get_json()
            userId = userService.userLogIn(UserLogInDto(body["email"], body["passwd"]))
            return ResponseDto(200, "로그인 완료", {"userId": json.loads(json_util.dumps(userId))["$oid"]}).toJSON(), 200
        except CustomException as e:
            return ErrorResponseDto(e.message, e.statusCode).toJSON()

    @route("/update", methods=["POST"])
    def userUpdateInfo(self):
        try:
            body = request.get_json()
            userService.userUpdateInfo(UserUpdateInfoDto(body["token"], body["name"]))
            return ResponseDto(200, "회원 정보 수정이 완료되었습니다.").toJSON(), 200
        except CustomException as e:
            return ErrorResponseDto(e.message, e.statusCode).toJSON()
