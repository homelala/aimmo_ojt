import datetime

from flask_mongoengine import Document
from mongoengine import StringField, IntField, DateField, ListField, ReferenceField, BooleanField

from app.domain.user import User


class Notice(Document):
    user = ReferenceField(User)
    id = StringField(required=False)
    title = StringField(required=True)
    description = StringField(required=True)
    register_date = DateField(default=datetime.datetime.now())
    like = IntField(default=0)
    tags = ListField(required=True)
    count_comments = IntField(default=0)
    is_deleted = BooleanField(default=False)

    @property
    def id(self):
        return self.__id

    def update_info(self, title, description, tags):
        self.update(title=title, description=description, tags=tags)

    def increase_like(self):
        self.update(like=self.like + 1)

    def increase_comment(self):
        self.update(count_comments=self.count_comments + 1)

    def delete_article(self):
        self.update(is_deleted=True)
