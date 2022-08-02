from marshmallow import fields, Schema, post_load

from marshmallow import fields, Schema, post_load

from app.domain.notice import Notice


class CommentUser(Schema):
    name = fields.String()


class CommentInfoSchema(Schema):
    description = fields.String(required=True)
    register_date = fields.String(required=True)
    user = fields.Nested(CommentUser())


class NoticeDetailSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    register_date = fields.String(required=True)
    like = fields.Integer(required=True)
    tags = fields.List(fields.String(), required=True)
    comments = fields.List(fields.Nested(CommentInfoSchema()))
    count_comments = fields.Integer()


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


class SearchArticleSchema(Schema):
    page = fields.Integer(required=True)
    title = fields.String(required=True)
    limit = fields.Integer(required=True)

    @post_load
    def make_param(self, data, **kwargs):
        return data

