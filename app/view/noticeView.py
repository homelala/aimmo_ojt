import json

from bson import ObjectId
from flask import g
from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView, request

from app.domain.NoticeComment import NoticeComment
from app.schema.reponse.ResponseDto import ResponseDto
from app.schema.NoticeCommentSchema import RegisterCommentSchema
from app.schema.NoticeSchema import NoticeSchema, RegisterArticleSchema, UpdateArticleSchema, NoticeDetailSchema
from app.schema.error.ApiErrorSchema import ApiErrorSchema
from app.schema.reponse.ResponseSchema import ResponseSchema, ResponseDictSchema
from app.service import noticeService
from app.utils.CustomException import CustomException
from app.utils.ErrorResponseDto import ErrorResponseDto

from app.utils.utils import valid_user, marshal_empty


class NoticeView(FlaskView):
    route_base = "/articles"
    decorators = (doc(tags=["Articles"]),)

    @route("/", methods=["POST"])
    @doc(description="article 등록", summary="article 등록")
    @valid_user
    # @use_kwargs(RegisterArticleSchema(), locations=("json",))
    @marshal_empty(code=200)
    def register_article(self, article=None):
        article = RegisterArticleSchema().load(json.loads(request.data))
        article.user = ObjectId(g.user_id)
        noticeService.register_article(article)
        return "", 200

    @route("/<article_id>", methods=["PUT"])
    @doc(description="article 수정", summary="article 수정")
    @valid_user
    @use_kwargs(UpdateArticleSchema(), locations=("json",))
    @marshal_empty(code=200)
    @marshal_with(ApiErrorSchema(), code=403, description="article 수정 실패")
    def update_article(self, data, article_id):
        try:
            data = UpdateArticleSchema().load(json.loads(request.data))
            noticeService.update_article(article_id, data)
            return "", 200
        except CustomException as e:
            return ErrorResponseDto(e.message), e.statusCode

    @route("/<article_id>", methods=["GET"])
    @doc(description="article 읽기", summary="article 읽기")
    @marshal_with(ResponseDictSchema(), code=200, description="article 불러오기")
    def read_article(self, article_id):
        article_info = noticeService.read_article(article_id)
        article_info.comments = NoticeComment.objects(notice=article_id)
        schema = NoticeDetailSchema()
        result = schema.dump(article_info)
        return ResponseDto(result), 200

    @route("/<article_id>", methods=["DELETE"])
    @valid_user
    @marshal_empty(code=200)
    def delete_article(self, article_id):
        noticeService.delete_article(article_id)
        return "", 200

    @route("/<article_id>/like", methods=["GET"])
    @doc(description="article 좋아요", summary="article 좋아요")
    @valid_user
    @marshal_empty(code=200)
    @marshal_with(ResponseSchema(), code=200, description="article 좋아요 완료")
    def like_article(self, article_id):
        noticeService.like_article(article_id)
        return "", 200

    @route("/<notice_id>/comment", methods=["POST"])
    @doc(description="article 댓글 달기", summary="article 댓글 달기")
    @valid_user
    # @use_kwargs(RegisterCommentSchema(), locations=("json",))
    @marshal_empty(code=200)
    @marshal_with(ResponseSchema(), code=200, description="article 댓글 달기 완료")
    def comment_article(self, notice_id, data=None):
        data = RegisterCommentSchema().load(json.loads(request.data))
        data.user = ObjectId(g.user_id)
        data.notice = ObjectId(notice_id)
        noticeService.comment_article(data)
        return "", 200

    @route("/search/<title>", methods=["GET"])
    @doc(description="article 검색", summary="article 검색")
    @marshal_with(ResponseSchema(), code=200, description="article 검색 완료")
    def search_article(self, title):
        article_list = noticeService.search_article(title)
        schema = NoticeSchema(many=True)
        return ResponseDto(schema.dump(article_list)), 200
