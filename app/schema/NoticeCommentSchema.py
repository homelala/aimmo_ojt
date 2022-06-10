from marshmallow import fields, Schema, post_load

from app.domain.NoticeComment import NoticeComment


class NoticeInfoSchema(Schema):
    title = fields.String(required=True)
    register_date = fields.String(required=True)


class NoticeCommentSchema(Schema):
    notice_id = fields.String(required=True)
    user_id = fields.String(required=True)
    description = fields.String(required=True)
    register_date = fields.String(required=True)
    notice = fields.List(fields.Nested(NoticeInfoSchema()))


class RegisterCommentSchema(Schema):
    notice_id = fields.String(required=False)
    user_id = fields.String(required=False)
    description = fields.String(required=False)

    @post_load()
    def newComment(self, data, **kwargs):
        comment = NoticeComment(**data)
        return comment
