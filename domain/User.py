class User:
    def __init__(self, name, email, passwd):
        self.__name = name
        self.__email = email
        self.__passwd = passwd

    @property
    def get__name(self):
        return self.__name

    @property
    def get__email(self):
        return self.__email

    @property
    def get__passwd(self):
        return self.__passwd
