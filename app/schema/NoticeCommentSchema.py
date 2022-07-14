from marshmallow import fields, Schema, post_load

from app.domain.NoticeComment import NoticeComment
from app.schema.NoticeSchema import NoticeInfoSchema


class NoticeCommentSchema(Schema):
    notice_id = fields.String(required=True)
    user_id = fields.String(required=True)
    description = fields.String(required=True)
    register_date = fields.String(required=True)
    notice = fields.List(fields.Nested(NoticeInfoSchema()))


class RegisterCommentSchema(Schema):
    description = fields.String(required=True)

    @post_load()
    def new_comment(self, data, **kwargs):
        comment = NoticeComment(**data)
        return comment
