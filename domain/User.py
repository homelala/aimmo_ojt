class User:
    def __init__(self, id=None, email=None, passwd=None, name=None, token=None):
        self.__id = id
        self.__name = name
        self.__email = email
        self.__passwd = passwd
        self.__token = token

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @property
    def passwd(self):
        return self.__passwd

    @property
    def token(self):
        return self.__token
