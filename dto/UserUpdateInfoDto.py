class UserUpdateInfoDto:
    def __init__(self, token, name):
        self.__token = token
        self.__name = name

    @property
    def token(self):
        return self.__token

    @property
    def name(self):
        return self.__name
