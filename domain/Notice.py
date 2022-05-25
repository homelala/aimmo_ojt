import datetime as dt
from flask_mongoengine import Document


class Notice(Document):
    def __init__(self, userId, title=None, description=None, noticeId=None, token=None, tags=None):
        self.__title = title
        self.__description = description
        self.__registerDate = dt.datetime.today()
        self.__userId = userId
        self.__token = token
        self.__noticeId = noticeId
        self.__like = 0
        self.__tags = tags

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def registerDate(self):
        return self.__registerDate

    @property
    def userId(self):
        return self.__userId

    @property
    def token(self):
        return self.__token

    @property
    def noticeId(self):
        return self.__noticeId

    @property
    def like(self):
        return self.__like

    @property
    def tags(self):
        return self.__tags
