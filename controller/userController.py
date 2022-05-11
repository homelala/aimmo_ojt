from bson import json_util
from flask import request, jsonify, Blueprint, make_response
import json

from dto.ResponseDto import ResponseDto
from dto.UserCreateDto import UserCreateDto
from dto.UserLogInDto import UserLogInDto
from service import userService
from utils.CustomException import CustomException
from utils.ErrorResponseDto import ErrorResponseDto

userApp = Blueprint("userApp", __name__)
# userApp.config["JSON_AS_ASCII"] = False


@userApp.route("/signUp", methods=["POST"])
def userSignUP():
    body = request.get_json()
    userId = userService.userSignUp(UserCreateDto(body["name"], body["email"], body["passwd"]))
    return ResponseDto(200, "회원 가입 완료", {"userId": json.loads(json_util.dumps(userId))["$oid"]}).toJSON(), 200


@userApp.route("/logIn", methods=["POST"])
def userLogIn():
    try:
        body = request.get_json()
        userId = userService.userLogIn(UserLogInDto(body["email"], body["passwd"]))
        return ResponseDto(200, "로그인 완료", {"userId": json.loads(json_util.dumps(userId))["$oid"]}).toJSON(), 200
    except CustomException as e:
        return ErrorResponseDto(e.message, e.statusCode).toJSON()
