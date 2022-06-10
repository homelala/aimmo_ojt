from marshmallow import fields, Schema, post_load
from mongoengine import ReferenceField

from app.domain.Notice import Notice
from app.domain.User import User


class CommentSchema(Schema):
    description = fields.String(required=True)
    register_date = fields.String(required=True)
    user_id = fields.String(required=True)
    notice_id = fields.String(required=True)


class NoticeSchema(Schema):
    title = fields.String(required=True)
    comments = fields.List(fields.Nested(CommentSchema()))
    description = fields.String(required=True)
    register_date = fields.String(required=True)
    user_id = fields.String(required=True)
    like = fields.Integer(required=True)
    tags = fields.List(fields.String())


class RegisterArticleSchema(Schema):
    title = fields.String(required=False)
    description = fields.String(required=False)
    user_id = fields.String(required=False)
    tags = fields.List(fields.String())

    @post_load
    def new_article(self, data, **kwargs):
        article = Notice(**data)
        return article


class UpdateArticleSchema(Schema):
    title = fields.String(required=False)
    description = fields.String(required=False)
    user_id = fields.String(required=False)
    tags = fields.List(fields.String())

    @post_load
    def updateNotice(self, data, **kwargs):
        print(data)
        article = Notice(**data)
        return article
