from marshmallow import fields, Schema, post_load

from domain.NoticeComment import NoticeComment
from funcy import project


class NoticeCommentSchema(Schema):
    noticeId = fields.String(required=True)
    userId = fields.String(required=True)
    description = fields.String(required=True)
    registerDate = fields.String(required=True)


class NoticeRegisterSchema(Schema):
    noticeId = fields.String(required=True)
    userId = fields.String(required=True)
    description = fields.String(required=True)
    token = fields.String(required=True)

    @post_load()
    def newComment(self, data, **kwargs):
        comment = NoticeComment(**project(data, ["noticeId", "userId", "description", "token"]))
        return comment
