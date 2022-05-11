class UserLogInDto:
    def __init__(self, email, passwd):
        self.__email = email
        self.__passwd = passwd

    @property
    def email(self):
        return self.__email

    @property
    def passwd(self):
        return self.__passwd
