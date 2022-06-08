from flask_apispec import marshal_with, doc
from flask_classful import route, FlaskView

from app.schema.reponse.ResponseDto import ResponseDto
from app.schema.NoticeCommentSchema import NoticeCommentSchema
from app.schema.NoticeSchema import NoticeSchema
from app.schema.error.ApiErrorSchema import ApiErrorSchema
from app.schema.reponse.ResponseSchema import ResponseSchema
from app.service import myPageService
from app.utils.CustomException import CustomException
from app.utils.ErrorResponseDto import ErrorResponseDto
import traceback

from app.utils.utils import valid_user


class MyPageController(FlaskView):
    route_base = "/my"
    decorators = (doc(tags=["Page"]),)

    @route("/<user_id>/articles", methods=["POST"])
    @doc(description="내가 작성한 게시물", summary="내가 작성한 게시물")
    @valid_user
    # @use_kwargs({"token": fields.String(required=True)}, locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="내가 작성한 게시물 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=400, description="내가 작성한 게시물 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def getMaxLikeNotice(self, user_id=None):
        try:
            notice_info = myPageService.get_my_articles(user_id)
            schema = NoticeSchema(many=True)
            return ResponseDto(200, "success", schema.dump(notice_info)), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/<user_id>/comments", methods=["POST"])
    @doc(description="내가 작성한 댓글", summary="내가 작성한 댓글")
    @valid_user
    # @use_kwargs({"token": fields.String(required=True)}, locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="내가 작성한 댓글 불러오기 성공")
    @marshal_with(ApiErrorSchema(), code=400, description="내가 작성한 댓글 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def getHighCommentNotice(self, user_id=None):
        try:
            notice_info = myPageService.get_my_comment(user_id)
            schema = NoticeCommentSchema(many=True)
            return ResponseDto(200, "success", schema.dump(notice_info)), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500
