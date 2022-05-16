from bson import json_util
from flask import request, g
import json
from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView
from dto.ResponseDto import ResponseDto
from schema.NoticeSchema import NoticeSchema, RegisterNoticeSchema
from schema.error.ApiErrorSchema import ApiErrorSchema
from schema.reponse.ResponseSchema import ResponseSchema
from service import noticeService
from utils.CustomException import CustomException
from utils.ErrorResponseDto import ErrorResponseDto


class NoticeController(FlaskView):
    route_base = "/notice"
    decorators = (doc(tags=["Notice"]),)

    @route("/register", methods=["POST"])
    @doc(description="Notice 등록", summary="Notice 등록")
    @use_kwargs(RegisterNoticeSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="notice 등록 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="notice 등록 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def registerNotice(self, notice=None):
        try:
            noticeService.registerNotice(notice)
            return ResponseDto(200, "공지 등록 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            print(e)
            return ErrorResponseDto(e, 500), 500
