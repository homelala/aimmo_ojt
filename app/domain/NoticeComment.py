import datetime

from flask_mongoengine import Document
from mongoengine import StringField, EmailField, IntField, DateField, ReferenceField

from app.domain.Notice import Notice
from app.domain.User import User


class NoticeComment(Document):
    user = ReferenceField(User)
    notice = ReferenceField(Notice)
    description = StringField(required=True)
    register_date = DateField(default=datetime.date.today())
    # user_id = StringField(required=True)
    # notice_id = StringField(required=True)
