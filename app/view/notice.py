from bson import ObjectId
from flask import g
from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView

from app.domain.notice import Notice
from app.domain.notice_comment import NoticeComment
from app.schema.notice import RegisterArticleSchema, UpdateArticleSchema, NoticeDetailSchema
from app.schema.notice_comment import RegisterCommentSchema
from app.schema.reponse.ResponseDto import ResponseDto
from app.schema.reponse.ResponseSchema import ResponseSchema, ResponseDictSchema
from app.utils.utils import valid_user, marshal_empty, valid_article_user, valid_article


class NoticeView(FlaskView):
    route_base = "/articles"
    decorators = (doc(tags=["Articles"]),)

    @route("/", methods=["POST"])
    @doc(description="article 등록", summary="article 등록")
    @valid_user
    @use_kwargs(RegisterArticleSchema(), locations=("json",))
    @marshal_empty(code=200)
    def register_article(self, article=None):
        article.user = ObjectId(g.user_id)
        Notice.save(article)
        return "", 200

    @route("/<article_id>", methods=["PUT"])
    @doc(description="article 수정", summary="article 수정")
    @valid_user
    @valid_article
    @valid_article_user
    @use_kwargs(UpdateArticleSchema(), locations=("json",))
    @marshal_empty(code=200)
    def update_article(self, article, article_id):
        article_info = Notice.objects(id=ObjectId(article_id)).get()
        article_info.update_info(article.title, article.description, article.tags)
        return "", 200

    @route("/<article_id>", methods=["GET"])
    @doc(description="article 읽기", summary="article 읽기")
    @valid_article
    @marshal_with(ResponseDictSchema(), code=200, description="article 불러오기")
    def read_article(self, article_id):
        article_info = Notice.objects(id=article_id).get()
        article_info.comments = NoticeComment.objects(notice=article_id)
        return ResponseDto(NoticeDetailSchema().dump(article_info)), 200

    @route("/<article_id>", methods=["DELETE"])
    @valid_user
    @valid_article
    @marshal_empty(code=200)
    def delete_article(self, article_id):
        comments = NoticeComment.objects(notice=article_id)
        for comment in comments:
            NoticeComment.delete(comment)
        article = Notice.objects(id=ObjectId(article_id)).get()
        Notice.delete(article)
        return "", 200

    @route("/<article_id>/like", methods=["GET"])
    @doc(description="article 좋아요", summary="article 좋아요")
    @valid_user
    @valid_article
    @marshal_empty(code=200)
    def like_article(self, article_id):
        Notice.objects(id=article_id).get().increase_like()
        return "", 200

    @route("/<article_id>/comment", methods=["POST"])
    @doc(description="article 댓글 달기", summary="article 댓글 달기")
    @valid_user
    @valid_article
    @use_kwargs(RegisterCommentSchema(), locations=("json",))
    @marshal_empty(code=200)
    def comment_article(self, data, article_id):
        data.user = ObjectId(g.user_id)
        data.notice = ObjectId(article_id)

        Notice.objects(id=article_id).get().increase_comment()
        NoticeComment.save(data)
        return "", 200

    @route("/search/<title>", methods=["GET"])
    @doc(description="article 검색", summary="article 검색")
    @marshal_with(ResponseSchema(), code=200, description="article 검색 완료")
    def search_article(self, title):
        article_list = Notice.objects(title__icontains=title).order_by("-register_date")
        schema = NoticeDetailSchema(many=True)
        return ResponseDto(schema.dump(article_list)), 200
