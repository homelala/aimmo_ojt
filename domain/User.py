class User:
    def __init__(self, name, email, passwd):
        self.__name = name
        self.__email = email
        self.__passwd = passwd

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @property
    def passwd(self):
        return self.__passwd
