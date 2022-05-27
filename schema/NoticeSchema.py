from bson import ObjectId
from marshmallow import fields, Schema, post_load, post_dump

from funcy import project

from domain.Notice import Notice
from domain.User import User


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
    title = fields.String(required=True)
    description = fields.String(required=True)
    user_id = fields.String(required=True)
    token = fields.String(required=True)
    tags = fields.List(fields.String())

    @post_load
    def new_article(self, data, **kwargs):
        article = Notice(title=data["title"], description=data["description"], user_id=data["user_id"], tags=data["tags"])
        return article


class UpdateArticleSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    user_id = fields.String(required=True)
    token = fields.String(required=True)
    tags = fields.List(fields.String())

    @post_load
    def updateNotice(self, data, **kwargs):
        article = Notice(title=data["title"], description=data["description"], user_id=data["user_id"], tags=data["tags"])
        return article
