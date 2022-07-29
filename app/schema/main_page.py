from marshmallow import Schema, fields, post_load


class MainPageParams(Schema):
    page = fields.Integer(required=True)
    category = fields.String(required=True)
    limit = fields.Integer(required=True)

    @post_load
    def make_param(self, data, **kwargs):
        return data
