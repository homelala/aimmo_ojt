import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory

from app.domain.Notice import Notice

from test.factory.user import UserFactory


class NoticeFactory(MongoEngineFactory):
    class Meta:
        model = Notice

    title = fuzzy.FuzzyText(length=10, prefix="post_")
    description = fuzzy.FuzzyText(length=20, prefix="post_")
    # user_id = id
    tags = ["test1", "test2"]
