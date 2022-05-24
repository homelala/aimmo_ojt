from flask_apispec import marshal_with, doc
from flask_classful import route, FlaskView

from schema.reponse.ResponseDto import ResponseDto
from schema.NoticeSchema import NoticeSchema
from schema.error.ApiErrorSchema import ApiErrorSchema
from schema.reponse.ResponseSchema import ResponseSchema
from service import noticeService
from utils.CustomException import CustomException
from utils.ErrorResponseDto import ErrorResponseDto
import traceback


class DashBoardController(FlaskView):
    route_base = "/main"
    decorators = (doc(tags=["Main"]),)

    @route("/like", methods=["GET"])
    @doc(description="상위 좋아요 게시물", summary="상위 좋아요 게시물")
    @marshal_with(ResponseSchema(), code=200, description="좋아요 상위 게시물 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=400, description="좋아요 상위 게시물 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def getMaxLikeNotice(self):
        try:
            notice_info = noticeService.get_high_like_article()
            schema = NoticeSchema(many=True)
            return ResponseDto(200, "success", schema.dump(notice_info)), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/comment", methods=["GET"])
    @doc(description="상위 댓글 게시물", summary="상위 댓글 게시물")
    @marshal_with(ResponseSchema(), code=200, description="댓글 상위 게시물 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=400, description="댓글 상위 게시물 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def getHighCommentNotice(self):
        try:
            noticeInfo = noticeService.get_high_comment_article()
            schema = NoticeSchema(many=True)
            return ResponseDto(200, "success", schema.dump(noticeInfo)), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/recent/articles", methods=["GET"])
    @doc(description="최근 게시물", summary="최근 게시물")
    @marshal_with(ResponseSchema(), code=200, description="최근 게시물 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=400, description="최근 게시물 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def getHighCommentNotice(self):
        try:
            notice_info = noticeService.get_recent_article()
            schema = NoticeSchema(many=True)
            return ResponseDto(200, "success", schema.dump(notice_info)), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500
