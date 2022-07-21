from flask_apispec import marshal_with, doc
from flask_classful import route, FlaskView

from app.domain.notice import Notice
from app.domain.notice_comment import NoticeComment
from app.schema.notice import NoticeDetailSchema
from app.schema.notice_comment import NoticeCommentSchema
from app.utils.utils import token_required


class MyPageView(FlaskView):
    route_base = "/my"
    decorators = (doc(tags=["Page"]),)

    @route("/<user_id>/articles", methods=["GET"])
    @doc(description="내가 작성한 게시물", summary="내가 작성한 게시물")
    @token_required
    @marshal_with(NoticeDetailSchema(many=True), code=200, description="내가 작성한 게시물 불러오기 성공")
    def my_articles(self, user_id=None):
        notice_info = Notice.objects(user=user_id).order_by("-register_date")
        schema = NoticeDetailSchema(many=True)
        return schema.dump(notice_info), 200

    @route("/<user_id>/comments", methods=["GET"])
    @doc(description="내가 작성한 댓글", summary="내가 작성한 댓글")
    @token_required
    @marshal_with(NoticeCommentSchema(many=True), code=200, description="내가 작성한 댓글 불러오기 성공")
    def my_comments(self, user_id=None):
        notice_info = NoticeComment.objects(user=user_id).select_related()
        schema = NoticeCommentSchema(many=True)
        return schema.dump(notice_info), 200
