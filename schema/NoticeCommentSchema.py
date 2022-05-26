from bson import ObjectId
from marshmallow import fields, Schema, post_load

from domain.NoticeComment import NoticeComment
from funcy import project

from domain.User import User


class NoticeInfoSchema(Schema):
    title = fields.String(required=True)
    registerDate = fields.String(required=True)


class NoticeCommentSchema(Schema):
    noticeId = fields.String(required=True)
    userId = fields.String(required=True)
    description = fields.String(required=True)
    registerDate = fields.String(required=True)
    notice = fields.List(fields.Nested(NoticeInfoSchema()))


class RegisterCommentSchema(Schema):
    notice_id = fields.String(required=True)
    user_id = fields.String(required=True)
    description = fields.String(required=True)
    token = fields.String(required=True)

    @post_load()
    def newComment(self, data, **kwargs):
        if User.objects(token=data["token"]).get().id != ObjectId(data["user_id"]):
            return False
        else:
            comment = NoticeComment(description=data["description"], user_id=data["user_id"], notice_id=data["notice_id"])
            return comment
