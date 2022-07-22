import datetime

from flask_mongoengine import Document
from mongoengine import StringField, DateField, ReferenceField, BooleanField

from app.domain.notice import Notice
from app.domain.user import User


class NoticeComment(Document):
    user = ReferenceField(User)
    notice = ReferenceField(Notice)
    description = StringField(required=True)
    register_date = DateField(default=datetime.date.today())
    is_deleted = BooleanField(default=False)

    def delete_comment(self):
        self.update(is_deleted=True)

