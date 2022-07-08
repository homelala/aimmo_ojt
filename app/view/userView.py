from bson import json_util
import json
import traceback
import logging

logger = logging.getLogger("test")
from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView, request
from app.schema.reponse.ResponseDto import ResponseDto
from app.schema.UserSchema import UserSignUpSchema, UserLogInSchema, UserUpdateInfoSchema
from app.schema.error.ApiErrorSchema import ApiErrorSchema
from app.schema.reponse.ResponseSchema import ResponseSchema, ResponseDictSchema
from app.service import userService
from app.utils.CustomException import CustomException
from app.utils.ErrorResponseDto import ErrorResponseDto
from app.utils.utils import valid_user


class UserView(FlaskView):
    route_base = "/user"
    decorators = (doc(tags=["User"]),)

    @route("/signUp", methods=["POST"])
    @doc(tags=["User"], description="User 회원 가입", summary="User 회원 가입")
    @use_kwargs(UserSignUpSchema(), locations=("json",))
    @marshal_with(ResponseDictSchema(), code=200, description="회원 가입 완료")
    @marshal_with(ApiErrorSchema(), code=402, description="회원 가입 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def signup(self, user):
        try:
            user = UserSignUpSchema().load(json.loads(request.data))
            user_info = userService.userSignUp(user)
            return ResponseDto(200, "회원 가입 성공", {"user_id": json.loads(json_util.dumps(user_info.id))["$oid"]}), 200
        except CustomException as e:
            return ErrorResponseDto(e.message, e.statusCode), e.statusCode
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e), 500

    @route("/logIn", methods=["POST"])
    @doc(description="User 로그인", summary="User 로그인")
    # @use_kwargs(UserLogInSchema(), locations=("json",))
    @marshal_with(ResponseDictSchema(), code=200, description="로그인 성공")
    @marshal_with(ApiErrorSchema(), code=401, description="로그인 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def login(self):
        try:
            data = json.loads(request.data)
            user = UserLogInSchema().load(data)
            user_info = userService.userLogIn(user, data["passwd"])
            return ResponseDto(200, "로그인 성공", {"userId": json.loads(json_util.dumps(user_info.id))["$oid"]}), 200
        except CustomException as e:
            return ErrorResponseDto(e.message, e.statusCode), e.statusCode
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e), 500

    @route("/", methods=["PUT"])
    @doc(description="User 정보 수정", summary="User 정보 수정")
    @valid_user
    @use_kwargs(UserUpdateInfoSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="정보 수정 성공")
    @marshal_with(ApiErrorSchema(), code=403, description="정보 수정 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def userUpdateInfo(self, user=None):
        try:
            user = UserUpdateInfoSchema().load(json.loads(request.data))
            userService.userUpdateInfo(user)
            return ResponseDto(200, "회원 정보 수정이 완료되었습니다.")
        except CustomException as e:
            return ErrorResponseDto(e.message, e.statusCode), e.statusCode
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e), 500
