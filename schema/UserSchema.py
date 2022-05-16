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


class UserSignUpSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    passwd = fields.String(required=True)

    @post_load
    def newUser(self, data, **kwargs):
        user = User(**project(data, ["email", "name", "passwd"]))
        return user


class UserLogInSchema(Schema):
    email = fields.Email(required=True)
    passwd = fields.String(required=True)

    @post_load
    def newUser(self, data, **kwargs):
        user = User(**project(data, ["email", "passwd"]))
        return user


class UserUpdateInfoSchema(Schema):
    id = fields.String(required=True)
    token = fields.String(required=True)
    name = fields.String(required=True)

    @post_load
    def newUser(self, data, **kwargs):
        user = User(**project(data, ["id", "name", "token"]))
        return user
