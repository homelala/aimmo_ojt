from marshmallow import fields, Schema, post_load

from app.domain.User import User


class UserSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    passwd = fields.String(required=True)

    @post_load
    def newUser(self, data, **kwargs):
        user = User(**data)
        return user


class UserSignUpSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    passwd = fields.String(required=True)

    @post_load
    def new_user(self, data, **kwargs):
        user = User(**data)
        return user


class UserLogInSchema(Schema):
    email = fields.Email(required=True)
    passwd = fields.String(required=True)

    @post_load
    def new_user(self, data, **kwargs):
        if not User.objects(email=data["email"]):
            return False
        else:
            return User.objects(email=data["email"]).get()


class UserUpdateInfoSchema(Schema):
    id = fields.String(required=True)
    token = fields.String(required=True)
    name = fields.String(required=True)

    @post_load
    def new_user(self, data, **kwargs):
        user = User(**data)
        return user