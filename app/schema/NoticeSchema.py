import json

from marshmallow import fields, Schema, post_load
from mongoengine import ReferenceField

from app.domain.Notice import Notice
from app.domain.NoticeComment import NoticeComment
from app.domain.User import User
from app.schema.NoticeCommentSchema import NoticeCommentSchema
from app.schema.UserSchema import UserSchema


class CommentSchema(Schema):
    description = fields.String(required=True)
    register_date = fields.String(required=True)
    user_name = fields.Method("get_user_name")

    def get_user_name(self, obt):
        return User.objects(id=obt.user.id).get()["name"]


class CommentDetailSchema(Schema):
    description = fields.String(required=True)
    register_date = fields.Date(required=True)
    user_name = fields.String(required=True)

    def __init__(self, comment):
        self.description = comment.description
        self.register_date = comment.register_date
        self.user_name = comment.user.name


class NoticeSchema(Schema):
    title = fields.String(required=True)
    comments = fields.List(fields.Nested(CommentSchema(many=True)))
    description = fields.String(required=True)
    register_date = fields.String(required=True)
    user_id = fields.String(required=True)
    like = fields.Integer(required=True)
    tags = fields.List(fields.String())


class NoticeDetailSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    register_date = fields.String(required=True)
    like = fields.Integer(required=True)
    tags = fields.List(fields.String())
    comments = fields.List(fields.Nested(CommentSchema()))

    def get_comments(self, obt):
        result = []
        print(obt.id)
        comment_list = NoticeComment.objects(notice=obt.id)
        for comment in comment_list:
            temp = CommentDetailSchema(comment)
            result.append(temp)
        return result


class RegisterArticleSchema(Schema):
    title = fields.String(required=False)
    description = fields.String(required=False)
    tags = fields.List(fields.String())

    @post_load
    def new_article(self, data, **kwargs):
        article = Notice(**data)
        return article


class UpdateArticleSchema(Schema):
    title = fields.String(required=False)
    description = fields.String(required=False)
    tags = fields.List(fields.String())

    @post_load
    def updateNotice(self, data, **kwargs):
        article = Notice(**data)
        return article
