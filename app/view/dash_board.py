from flask_apispec import marshal_with, doc, use_kwargs
from flask_classful import route, FlaskView
from marshmallow import fields

from app.domain.notice import Notice
from app.schema.notice import NoticeDetailSchema
from app.schema.reponse.ResponseDto import ResponseDto
from app.schema.reponse.ResponseSchema import ResponseSchema


class DashBoardView(FlaskView):
    route_base = "/main"
    decorators = (doc(tags=["Main"]),)

    @route("/top", methods=["GET"])
    @doc(description="상위 게시물", summary="상위 좋아요 게시물")
    @use_kwargs({"category": fields.String(), "page": fields.Integer(), "limit": fields.Integer()}, location="querystring")
    @marshal_with(ResponseSchema(), code=200, description="카테고리별 상위 게시물 불러오기 성공")
    def top_articles(self, page, limit, category):
        notice_info = Notice.objects().order_by("-" + category).skip((page - 1) * 10).limit(limit)
        schema = NoticeDetailSchema(many=True)
        return ResponseDto(schema.dump(notice_info)), 200
