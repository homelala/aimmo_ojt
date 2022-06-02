import datetime

from flask_mongoengine import Document
from mongoengine import StringField, EmailField, IntField, DateField


class NoticeComment(Document):
    description = StringField(required=True)
    register_date = DateField(default=datetime.date.today())
    user_id = StringField(required=True)
    notice_id = StringField(required=True)
