from marshmallow import fields, Schema, post_load, post_dump

from funcy import project

from domain.Notice import Notice


class CommentSchema(Schema):
    description = fields.String(required=True)
    registerDate = fields.String(required=True)
    userId = fields.String(required=True)
    noticeId = fields.String(required=True)


class NoticeSchema(Schema):
    noticedId = fields.String(required=True)
    title = fields.String(required=True)
    comments = fields.List(fields.Nested(CommentSchema()))
    description = fields.String(required=True)
    registerDate = fields.String(required=True)
    userId = fields.String(required=True)
    like = fields.Integer(required=True)
    tags = fields.List(fields.String())


class RegisterNoticeSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    userId = fields.String(required=True)
    token = fields.String(required=True)
    tags = fields.List(fields.String())

    @post_load
    def newNotice(self, data, **kwargs):
        notice = Notice(**project(data, ["title", "description", "userId", "token", "tags"]))
        return notice


class UpdateNoticeSchema(Schema):
    noticeId = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    userId = fields.String(required=True)
    token = fields.String(required=True)
    tags = fields.List(fields.String())

    @post_load
    def updateNotice(self, data, **kwargs):
        notice = Notice(**project(data, ["noticeId", "title", "description", "userId", "token", "tags"]))
        return notice


class LikeNoticeSchema(Schema):
    noticeId = fields.String(required=True)
    userId = fields.String(required=True)
    token = fields.String(required=True)

    @post_load
    def likeNotice(self, data, **kwargs):
        notice = Notice(**project(data, ["noticeId", "userId", "token"]))
        return notice
