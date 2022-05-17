import datetime as dt


class NoticeComment:
    def __init__(self, userId, description, noticeId, token):
        self.__description = description
        self.__registerDate = dt.datetime.today()
        self.__userId = userId
        self.__token = token
        self.__noticeId = noticeId

    @property
    def userId(self):
        return self.__userId

    @property
    def description(self):
        return self.__description

    @property
    def noticeId(self):
        return self.__noticeId

    @property
    def token(self):
        return self.__token

    @property
    def registerDate(self):
        return self.__registerDate
