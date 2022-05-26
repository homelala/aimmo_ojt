from bson import ObjectId
from marshmallow import fields, Schema, post_load, post_dump

from funcy import project

from domain.Notice import Notice
from domain.User import User


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


class RegisterArticleSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    user_id = fields.String(required=True)
    token = fields.String(required=True)
    tags = fields.List(fields.String())

    @post_load
    def new_article(self, data, **kwargs):
        print(type(User.objects(token=data["token"]).get().id), type(data["user_id"]))
        if User.objects(token=data["token"]).get().id != ObjectId(data["user_id"]):
            return False
        else:
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
        print(type(User.objects(token=data["token"]).get().id), type(data["user_id"]))
        if User.objects(token=data["token"]).get().id != ObjectId(data["user_id"]):
            return False
        else:
            article = Notice(title=data["title"], description=data["description"], user_id=data["user_id"], tags=data["tags"])
            return article


class LikeNoticeSchema(Schema):
    user_id = fields.String(required=True)
    token = fields.String(required=True)

    @post_load
    def likeNotice(self, data, **kwargs):
        notice = Notice(**project(data, ["noticeId", "userId", "token"]))
        return notice
