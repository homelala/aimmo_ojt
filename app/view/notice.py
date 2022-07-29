from bson import ObjectId
from flask import g
from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView
from marshmallow import fields

from app.domain.notice import Notice
from app.domain.notice_comment import NoticeComment
from app.schema.notice import RegisterArticleSchema, UpdateArticleSchema, NoticeDetailSchema
from app.schema.notice_comment import RegisterCommentSchema
from app.utils.utils import token_required, marshal_empty, valid_article_user, valid_article


class NoticeView(FlaskView):
    route_base = "/articles"
    decorators = (doc(tags=["Articles"]),)

    @route("/", methods=["POST"])
    @doc(description="article 등록", summary="article 등록")
    @token_required
    @use_kwargs(RegisterArticleSchema(), locations=["json"])
    @marshal_empty(code=201)
    def post(self, article=None):
        article.user = ObjectId(g.user_id)
        Notice.save(article)
        return "", 201

    @route("/<article_id>", methods=["PUT"])
    @doc(description="article 수정", summary="article 수정")
    @token_required
    @valid_article
    @valid_article_user
    @use_kwargs(UpdateArticleSchema(), locations=["json"])
    @marshal_empty(code=200)
    def update(self, article, article_id):
        article_info = Notice.objects(id=ObjectId(article_id)).get()
        article_info.update_info(article.title, article.description, article.tags)
        return "", 200

    @route("/<article_id>", methods=["GET"])
    @doc(description="article 읽기", summary="article 읽기")
    @valid_article
    @marshal_with(NoticeDetailSchema(), code=200, description="article 불러오기")
    def get(self, article_id):
        article_info = Notice.objects(id=article_id).get()
        article_info.comments = NoticeComment.objects(notice=article_id)
        return NoticeDetailSchema().dump(article_info), 200

    @route("/<article_id>", methods=["DELETE"])
    @token_required
    @valid_article
    @marshal_empty(code=200)
    def delete(self, article_id):
        comments = NoticeComment.objects(notice=ObjectId(article_id))
        for comment in comments:
            comment.delete_comment()
        Notice.objects(id=ObjectId(article_id)).get().delete_article()
        return "", 200

    @route("/<article_id>/like", methods=["GET"])
    @doc(description="article 좋아요", summary="article 좋아요")
    @token_required
    @valid_article
    @marshal_empty(code=200)
    def like(self, article_id):
        Notice.objects(id=ObjectId(article_id)).get().increase_like()
        return "", 200

    @route("/<article_id>/comment", methods=["POST"])
    @doc(description="article 댓글 달기", summary="article 댓글 달기")
    @token_required
    @valid_article
    @use_kwargs(RegisterCommentSchema(), locations=["json"])
    @marshal_empty(code=201)
    def comment(self, data, article_id):
        data.user = ObjectId(g.user_id)
        data.notice = ObjectId(article_id)

        Notice.objects(id=article_id).get().increase_comment()
        NoticeComment.save(data)
        return "", 201

    @route("/search", methods=["GET"])
    @doc(description="article 검색", summary="article 검색")
    # @use_kwargs({"title": fields.String(), "page": fields.Integer(), "limit": fields.Integer()})
    @marshal_with(NoticeDetailSchema(many=True), code=200, description="article 검색 완료")
    def search(self, title, page, limit):
        article_list = Notice.objects(title__icontains=title, is_deleted=False).order_by("-register_date").skip((page-1)*10).limit(limit)
        schema = NoticeDetailSchema(many=True)
        return schema.dump(article_list), 200
