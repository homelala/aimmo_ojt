from bson import json_util
from flask import request, jsonify, Blueprint
import json

from dto.UserCreateDto import UserCreateDto
from service import userService

userApp = Blueprint("userApp", __name__)


@userApp.route("/signUp", methods=["POST"])
def userSignUP():
    body = request.get_json()
    userId = userService.userSignUp(UserCreateDto(body["name"], body["email"], body["passwd"]))
    return jsonify(200, "회원 가입 완료", {"userId": json.loads(json_util.dumps(userId))["$oid"]}), 200
