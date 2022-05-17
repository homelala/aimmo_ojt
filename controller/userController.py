from bson import json_util
import json
import traceback
from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView
from dto.ResponseDto import ResponseDto
from schema.UserSchema import UserSchema, UserSignUpSchema, UserLogInSchema, UserUpdateInfoSchema
from schema.error.ApiErrorSchema import ApiErrorSchema
from schema.reponse.ResponseSchema import ResponseSchema
from service import userService
from utils.CustomException import CustomException
from utils.ErrorResponseDto import ErrorResponseDto


class UserController(FlaskView):
    route_base = "/user"
    decorators = (doc(tags=["User"]),)

    @route("/signUp", methods=["POST"])
    @doc(description="User 회원 가입", summary="User 회원 가입")
    @use_kwargs(UserSignUpSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="회원 가입 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="회원 가입 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def userSignUP(self, user=None):
        try:
            userId = userService.userSignUp(user)
            return ResponseDto(200, "회원 가입 완료", {"userId": json.loads(json_util.dumps(userId))["$oid"]}), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e), 500

    @route("/logIn", methods=["POST"])
    @doc(description="User 로그인", summary="User 로그인")
    @use_kwargs(UserLogInSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="로그인 성공")
    @marshal_with(ApiErrorSchema(), code=400, description="로그인 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def userLogIn(self, user=None):
        try:
            userId = userService.userLogIn(user.email, user.passwd)
            return ResponseDto(200, "로그인 완료", {"userId": json.loads(json_util.dumps(userId))["$oid"]}), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e), 500

    @route("/update", methods=["POST"])
    @doc(description="User 정보 수정", summary="User 정보 수정")
    @use_kwargs(UserUpdateInfoSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="정보 수정 성공")
    @marshal_with(ApiErrorSchema(), code=400, description="정보 수정 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def userUpdateInfo(self, user=None):
        try:
            userService.userUpdateInfo(user)
            return ResponseDto(200, "회원 정보 수정이 완료되었습니다.")
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e), 500
