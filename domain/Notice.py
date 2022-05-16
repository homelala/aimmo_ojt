import datetime as dt


class Notice:
    def __init__(self, title, description, userId, token=None):
        self.__title = title
        self.__description = description
        self.__registerDate = dt.date.today()
        self.__userId = userId
        self.__token = token

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
