from flask_apispec import marshal_with, doc, use_kwargs
from flask_classful import route, FlaskView

from app.domain.notice import Notice
from app.schema.main_page import MainPageParams
from app.schema.notice import NoticeDetailSchema


class DashBoardView(FlaskView):
    route_base = "/main"
    decorators = (doc(tags=["Main"]),)

    @route("/top", methods=["GET"])
    @doc(description="상위 게시물", summary="상위 좋아요 게시물")
    @use_kwargs(MainPageParams, locations=["query"])
    @marshal_with(NoticeDetailSchema(many=True), code=200, description="카테고리별 상위 게시물 불러오기 성공")
    def top_articles(self, page, limit, category):
        notice_info = Notice.objects(is_deleted=False).order_by("-" + category).skip((page - 1) * 10).limit(limit)
        schema = NoticeDetailSchema(many=True)
        return schema.dump(notice_info), 200
