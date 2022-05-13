from marshmallow import fields, Schema, post_load

from domain.User import User
from funcy import project


class UserSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    passwd = fields.String(required=True)

    @post_load
    def newUser(self, data, **kwargs):
        user = User(**project(data, ["email", "name", "passwd"]))
        return user
