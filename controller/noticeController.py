from flask_apispec import use_kwargs, marshal_with, doc
from marshmallow import fields
from flask_classful import route, FlaskView, request
from dto.ResponseDto import ResponseDto
from schema.NoticeCommentSchema import NoticeRegisterSchema
from schema.NoticeSchema import NoticeSchema, RegisterArticleSchema, LikeNoticeSchema, UpdateArticleSchema
from schema.error.ApiErrorSchema import ApiErrorSchema
from schema.reponse.ResponseSchema import ResponseSchema, ResponseDictSchema
from service import noticeService
from utils.CustomException import CustomException
from utils.ErrorResponseDto import ErrorResponseDto
import traceback
import json
from pprint import pprint


class NoticeController(FlaskView):
    route_base = "/articles"
    decorators = (doc(tags=["Articles"]),)

    @route("/", methods=["POST"])
    @doc(description="Notice 등록", summary="Notice 등록")
    @use_kwargs(RegisterArticleSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="notice 등록 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="notice 등록 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def registerNotice(self, notice=None):
        try:
            noticeService.register_article(notice)
            return ResponseDto(200, "공지 등록 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/<article_id>", methods=["PUT"])
    @doc(description="Notice 수정", summary="Notice 수정")
    @marshal_with(ResponseSchema(), code=200, description="notice 수정 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="notice 수정 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def updateNotice(self, article_id):
        try:
            data = UpdateArticleSchema().load(json.loads(request.data))
            noticeService.update_article(article_id, data)
            return ResponseDto(200, "공지 수정 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/<article_id>", methods=["GET"])
    @doc(description="Notice 읽기", summary="Notice 읽기")
    @marshal_with(ResponseDictSchema(), code=200, description="notice 불러오기")
    @marshal_with(ApiErrorSchema(), code=400, description="notice 불러오기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def readNotice(self, article_id):
        try:
            notice_info = noticeService.read_article(article_id)
            schema = NoticeSchema()
            return ResponseDto(200, "success", schema.dump(notice_info)), 200

        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/<article_id>", methods=["DELETE"])
    @doc(description="Notice 삭제", summary="Notice 삭제")
    @marshal_with(ResponseSchema(), code=200, description="notice 삭제 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="notice 삭제 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def delete(self, article_id):
        try:
            noticeService.delete_article(article_id)
            return ResponseDto(200, "공지 삭제 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/like", methods=["POST"])
    @doc(description="Notice 좋아요", summary="Notice 좋아요")
    @use_kwargs(LikeNoticeSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="notice 좋아요 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="notice 좋아요 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def likeNotice(self, notice):
        try:
            noticeService.like_notice(notice.userId, notice.token, notice.noticeId)
            return ResponseDto(200, "좋아요 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/comment", methods=["POST"])
    @doc(description="Notice 댓글 달기", summary="Notice 댓글 달기")
    @use_kwargs(NoticeRegisterSchema(), locations=("json",))
    @marshal_with(ResponseSchema(), code=200, description="notice 댓글 달기 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="notice 댓글 달기 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def likeNotice(self, notice):
        try:
            noticeService.comment_notice(notice)
            return ResponseDto(200, "댓글 달기 완료"), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500

    @route("/search/<title>", methods=["GET"])
    @doc(description="Notice 검색", summary="Notice 검색")
    @marshal_with(ResponseSchema(), code=200, description="notice 검색 완료")
    @marshal_with(ApiErrorSchema(), code=400, description="notice 검색 실패")
    @marshal_with(ApiErrorSchema(), code=500, description="INTERNAL_SERVER_ERROR")
    def likeNotice(self, title):
        try:
            notice_list = noticeService.search_notice(title)
            schema = NoticeSchema(many=True)
            return ResponseDto(200, "success", schema.dump(notice_list)), 200
        except CustomException as e:
            return ErrorResponseDto(e.message), 400
        except Exception as e:
            traceback.print_exc()
            return ErrorResponseDto(e, 500), 500
