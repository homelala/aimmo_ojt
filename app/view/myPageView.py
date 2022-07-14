from flask_apispec import marshal_with, doc
from flask_classful import route, FlaskView

from app.domain.Notice import Notice
from app.domain.NoticeComment import NoticeComment
from app.schema.NoticeCommentSchema import NoticeCommentSchema
from app.schema.NoticeSchema import NoticeDetailSchema
from app.schema.reponse.ResponseDto import ResponseDto
from app.schema.reponse.ResponseSchema import ResponseSchema
from app.utils.utils import valid_user


class MyPageView(FlaskView):
    route_base = "/my"
    decorators = (doc(tags=["Page"]),)

    @route("/<user_id>/articles", methods=["GET"])
    @doc(description="내가 작성한 게시물", summary="내가 작성한 게시물")
    @valid_user
    @marshal_with(ResponseSchema(), code=200, description="내가 작성한 게시물 불러오기 성공")
    def getMaxLikeNotice(self, user_id=None):
        notice_info = Notice.objects(user=user_id).order_by("-register_date")
        schema = NoticeDetailSchema(many=True)
        return ResponseDto(schema.dump(notice_info)), 200

    @route("/<user_id>/comments", methods=["GET"])
    @doc(description="내가 작성한 댓글", summary="내가 작성한 댓글")
    @valid_user
    @marshal_with(ResponseSchema(), code=200, description="내가 작성한 댓글 불러오기 성공")
    def getHighCommentNotice(self, user_id=None):
        notice_info = NoticeComment.objects(user=user_id)
        schema = NoticeCommentSchema(many=True)
        return ResponseDto(schema.dump(notice_info)), 200
