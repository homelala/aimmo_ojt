class UserCreateDto:
    def __init__(self, name, email, passwd):
        print(name, email, passwd)
        self._name = name
        self._email = email
        self._passwd = passwd

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def passwd(self):
        return self._passwd
