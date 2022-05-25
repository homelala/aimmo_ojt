import datetime
from flask_mongoengine import Document
from mongoengine import StringField, IntField, DateField, ListField


class Notice(Document):
    id = StringField(required=False)
    title = StringField(required=True)
    description = StringField(required=True)
    register_date = DateField(default=datetime.datetime.now())
    user_id = StringField(required=True)
    like = IntField(default=0)
    tags = ListField(required=True)
