from flask_apispec import use_kwargs, marshal_with, doc
from marshmallow import fields, Schema, post_load
from flask_classful import route, FlaskView
from dto.ResponseDto import ResponseDto
from schema.NoticeSchema import NoticeSchema, RegisterNoticeSchema, UpdateNoticeSchema
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

    @route("/update", methods=["POST"])
    @doc(description="Notice 수정", summary="Notice 수정")
    @use_kwargs(UpdateNoticeSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="notice 수정 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="notice 수정 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def updateNotice(self, notice=None):
        try:
            noticeService.updateNotice(notice)
            return ResponseDto(200, "공지 수정 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            print(e)
            return ErrorResponseDto(e, 500), 500

    @route("/read/<noticeId>", methods=["GET"])
    @doc(description="Notice 읽기", summary="Notice 읽기")
    @marshal_with(NoticeSchema(), code=200, description="notice 불러오기")
    @marshal_with(ApiErrorSchema(), code=400, description="notice 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def readNotice(self, noticeId):
        try:
            noticeInfo = noticeService.readNotice(noticeId)
            print(noticeInfo)
            schema = NoticeSchema()
            print(schema.dump(noticeInfo))
            return schema.dump(noticeInfo), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            print(e)
            return ErrorResponseDto(e, 500), 500

    @route("/delete", methods=["DELETE"])
    @doc(description="Notice 읽기", summary="Notice 읽기")
    @use_kwargs({"noticeId": fields.String(required=True), "userId": fields.String(required=True)}, locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="notice 삭제 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="notice 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def delete(self, userId, noticeId):
        try:
            print(userId)
            noticeService.deleteNotice(userId, noticeId)
            return ResponseDto(200, "공지 삭제 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            print(e)
            return ErrorResponseDto(e, 500), 500
