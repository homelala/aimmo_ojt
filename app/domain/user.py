from flask_mongoengine import Document
from mongoengine import StringField, EmailField


class User(Document):
    id = StringField(required=False)
    name = StringField(required=True)
    email = EmailField(required=False, unique=True)
    passwd = StringField(required=False)
    token = StringField(required=False)

    @property
    def id(self):
        return self.__id

    @property
    def user_email(self):
        return self.email

    def check_passwd(self, passwd):
        if self.passwd != passwd:
            return False
        return True

    def update_token(self, token):
        self.update(token=token)

    def update_name(self, name):
        self.update(name=name)
