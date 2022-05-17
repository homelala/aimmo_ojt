from marshmallow import fields, Schema, post_load

from funcy import project

from domain.Notice import Notice


class NoticeSchema(Schema):
    title = fields.String()
    description = fields.String()
    registerDate = fields.String()
    userId = fields.String()
    like = fields.Integer()


class RegisterNoticeSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    userId = fields.String(required=True)
    token = fields.String(required=True)

    @post_load
    def newNotice(self, data, **kwargs):
        notice = Notice(**project(data, ["title", "description", "userId", "token"]))
        return notice


class UpdateNoticeSchema(Schema):
    noticeId = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    userId = fields.String(required=True)
    token = fields.String(required=True)

    @post_load
    def updateNotice(self, data, **kwargs):
        notice = Notice(**project(data, ["noticeId", "title", "description", "userId", "token"]))
        return notice


class LikeNoticeSchema(Schema):
    noticeId = fields.String(required=True)
    userId = fields.String(required=True)
    token = fields.String(required=True)

    @post_load
    def likeNotice(self, data, **kwargs):
        notice = Notice(**project(data, ["noticeId", "userId", "token"]))
        return notice
