import datetime
from flask_mongoengine import Document
from mongoengine import StringField, IntField, DateField, ListField, ReferenceField

from app.domain.User import User


class Notice(Document):
    id = StringField(required=False)
    title = StringField(required=True)
    description = StringField(required=True)
    register_date = DateField(default=datetime.datetime.now())
    user_id = StringField(required=True)
    # user = ReferenceField(User)
    like = IntField(default=0)
    tags = ListField(required=True)

    @property
    def id(self):
        return self.__id

    def update_info(self, title, description, tags):
        self.update(title=title, description=description, tags=tags)

    def update_like(self):
        self.update(like=self.like + 1)


#
