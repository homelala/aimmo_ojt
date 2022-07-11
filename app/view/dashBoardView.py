from flask_apispec import marshal_with, doc
from flask_classful import route, FlaskView
from app.schema.reponse.ResponseDto import ResponseDto
from app.schema.NoticeSchema import NoticeSchema
from app.schema.error.ApiErrorSchema import ApiErrorSchema
from app.schema.reponse.ResponseSchema import ResponseSchema
from app.service import noticeService
from app.utils.ErrorResponseDto import ErrorResponseDto
import traceback


class DashBoardView(FlaskView):
    route_base = "/main"
    decorators = (doc(tags=["Main"]),)

    @route("/like", methods=["GET"])
    @doc(description="상위 좋아요 게시물", summary="상위 좋아요 게시물")
    @marshal_with(ResponseSchema(), code=200, description="좋아요 상위 게시물 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def get_high_like_articles(self):
        try:
            notice_info = noticeService.get_high_like_article()
            schema = NoticeSchema(many=True)
            return ResponseDto(200, "success", schema.dump(notice_info)), 200
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/comment", methods=["GET"])
    @doc(description="상위 댓글 게시물", summary="상위 댓글 게시물")
    @marshal_with(ResponseSchema(), code=200, description="댓글 상위 게시물 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def get_high_comment_articles(self):
        try:
            notice_info = noticeService.get_high_comment_article()
            schema = NoticeSchema(many=True)
            return ResponseDto(200, "success", schema.dump(notice_info)), 200
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/recent/articles", methods=["GET"])
    @doc(description="최근 게시물", summary="최근 게시물")
    @marshal_with(ResponseSchema(), code=200, description="최근 게시물 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def get_recent_articles(self):
        try:
            notice_info = noticeService.get_recent_article()
            schema = NoticeSchema(many=True)
            return ResponseDto(200, "success", schema.dump(notice_info)), 200
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500
