from marshmallow import fields, Schema, post_load

from funcy import project

from schema.reponse.ResponseDto import ResponseDto


class ResponseSchema(Schema):
    statusCode = fields.Integer(required=True)
    message = fields.String(required=True)
    data = fields.List(fields.Dict())

    @post_load
    def newResponseDto(self, data, **kwargs):
        responseDto = ResponseDto(**project(data, ["statusCode", "message", "data"]))
        return responseDto


class ResponseDictSchema(Schema):
    statusCode = fields.Integer(required=True)
    message = fields.String(required=True)
    data = fields.Dict()

    @post_load
    def newResponseDto(self, data, **kwargs):
        responseDto = ResponseDto(**project(data, ["statusCode", "message", "data"]))
        return responseDto
