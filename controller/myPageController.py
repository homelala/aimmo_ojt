from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView
from marshmallow import fields

from dto.ResponseDto import ResponseDto
from schema.NoticeCommentSchema import NoticeCommentSchema
from schema.NoticeSchema import NoticeSchema
from schema.error.ApiErrorSchema import ApiErrorSchema
from schema.reponse.ResponseSchema import ResponseSchema
from service import myPageService
from utils.CustomException import CustomException
from utils.ErrorResponseDto import ErrorResponseDto
import traceback


class MyPageController(FlaskView):
    route_base = "/page"
    decorators = (doc(tags=["Page"]),)

    @route("/articles", methods=["POST"])
    @doc(description="내가 작성한 게시물", summary="내가 작성한 게시물")
    @use_kwargs({"userId": fields.String(required=True), "token": fields.String(required=True)}, locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="내가 작성한 게시물 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=400, description="내가 작성한 게시물 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def getMaxLikeNotice(self, userId=None, token=None):
        try:
            noticeInfo = myPageService.getMyNotice(userId, token)
            schema = NoticeSchema(many=True)
            return ResponseDto(200, "success", schema.dump(noticeInfo)), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/comments", methods=["POST"])
    @doc(description="내가 작성한 댓글", summary="내가 작성한 댓글")
    @use_kwargs({"userId": fields.String(required=True), "token": fields.String(required=True)}, locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="내가 작성한 댓글 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=400, description="내가 작성한 댓글 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def getHighCommentNotice(self, userId=None, token=None):
        try:
            noticeInfo = myPageService.getMyComment(userId, token)
            schema = NoticeCommentSchema(many=True)
            return ResponseDto(200, "success", schema.dump(noticeInfo)), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500
