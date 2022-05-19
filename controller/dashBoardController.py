from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView

from schema.NoticeSchema import NoticeSchema, RegisterNoticeSchema, UpdateNoticeSchema, LikeNoticeSchema
from schema.error.ApiErrorSchema import ApiErrorSchema
from service import noticeService
from utils.CustomException import CustomException
from utils.ErrorResponseDto import ErrorResponseDto
import traceback
from pprint import pprint


class DashBoardController(FlaskView):
    route_base = "/main"
    decorators = (doc(tags=["Main"]),)

    @route("/like", methods=["GET"])
    @doc(description="상위 좋아요 게시물", summary="상위 좋아요 게시물")
    @marshal_with(NoticeSchema(many=True), code=200, description="좋아요 상위 게시물 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=400, description="좋아요 상위 게시물 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def getMaxLikeNotice(self):
        try:
            noticeInfo = noticeService.getMaxLikeNotice()
            pprint(noticeInfo)
            schema = NoticeSchema(many=True)
            return schema.dump(noticeInfo), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/comment", methods=["GET"])
    @doc(description="상위 댓글 게시물", summary="상위 댓글 게시물")
    @marshal_with(NoticeSchema(many=True), code=200, description="댓글 상위 게시물 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=400, description="댓글 상위 게시물 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def getHighCommentNotice(self):
        try:
            noticeInfo = noticeService.getHighCommentNotice()
            schema = NoticeSchema(many=True)
            return schema.dump(noticeInfo), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500
