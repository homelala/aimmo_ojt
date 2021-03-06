from factory.mongoengine import MongoEngineFactory

from app.domain.notice_comment import NoticeComment
from factory import fuzzy


class NoticeCommentFactory(MongoEngineFactory):
    class Meta:
        model = NoticeComment

    description = fuzzy.FuzzyText(length=20)
