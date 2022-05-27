from flask_apispec import use_kwargs, marshal_with, doc
from flask_classful import route, FlaskView, request
from schema.reponse.ResponseDto import ResponseDto
from schema.NoticeCommentSchema import RegisterCommentSchema
from schema.NoticeSchema import NoticeSchema, RegisterArticleSchema, LikeNoticeSchema, UpdateArticleSchema
from schema.error.ApiErrorSchema import ApiErrorSchema
from schema.reponse.ResponseSchema import ResponseSchema, ResponseDictSchema
from service import noticeService
from utils.CustomException import CustomException
from utils.ErrorResponseDto import ErrorResponseDto
import traceback

from utils.utils import valid_user


class NoticeController(FlaskView):
    route_base = "/articles"
    decorators = (doc(tags=["Articles"]),)

    @route("/", methods=["POST"])
    @doc(description="article 등록", summary="article 등록")
    @valid_user
    @use_kwargs(RegisterArticleSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="article 등록 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="article 등록 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def register_article(self, article=None):
        try:
            noticeService.register_article(article)
            return ResponseDto(200, "공지 등록 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/<article_id>", methods=["PUT"])
    @doc(description="article 수정", summary="article 수정")
    @valid_user
    @use_kwargs(UpdateArticleSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="article 수정 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="article 수정 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def update_article(self, data, article_id):
        try:
            noticeService.update_article(article_id, data)
            return ResponseDto(200, "공지 수정 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/<article_id>", methods=["GET"])
    @doc(description="article 읽기", summary="article 읽기")
    @marshal_with(ResponseDictSchema(), code=200, description="article 불러오기")
    @marshal_with(ApiErrorSchema(), code=400, description="article 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def read_article(self, article_id):
        try:
            article_info = noticeService.read_article(article_id)
            schema = NoticeSchema()
            return ResponseDto(200, "success", schema.dump(article_info)), 200

        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/<article_id>", methods=["DELETE"])
    @doc(description="article 삭제", summary="article 삭제")
    @marshal_with(ResponseSchema(), code=200, description="article 삭제 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="article 삭제 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def delete_article(self, article_id):
        try:
            noticeService.delete_article(article_id)
            return ResponseDto(200, "공지 삭제 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/<article_id>/like", methods=["POST"])
    @doc(description="article 좋아요", summary="article 좋아요")
    @use_kwargs(LikeNoticeSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="article 좋아요 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="article 좋아요 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def like_article(self, data, article_id):
        try:
            noticeService.like_article(article_id, data)
            return ResponseDto(200, "좋아요 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/comment", methods=["POST"])
    @doc(description="article 댓글 달기", summary="article 댓글 달기")
    @use_kwargs(RegisterCommentSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="article 댓글 달기 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="article 댓글 달기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def comment_article(self, data):
        try:
            noticeService.comment_article(data)
            return ResponseDto(200, "댓글 달기 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/search/<title>", methods=["GET"])
    @doc(description="article 검색", summary="article 검색")
    @marshal_with(ResponseSchema(), code=200, description="article 검색 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="article 검색 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def search_article(self, title):
        try:
            article_list = noticeService.search_article(title)
            schema = NoticeSchema(many=True)
            return ResponseDto(200, "success", schema.dump(article_list)), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500
