from marshmallow import fields, Schema


class ApiErrorSchema(Schema):
    statusCode = fields.Integer(data_key="code", required=True)
    message = fields.String(required=True)
