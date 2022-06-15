class CustomException(Exception):
    def __init__(self, statusCode, message):
        self.__statusCode = statusCode
        self.__message = message

    @property
    def statusCode(self):
        return self.__statusCode

    @property
    def message(self):
        return self.__message


class NotExistUserException(CustomException):
    def __init__(self, message):
        statusCode = 401
        self.__message = message
        super().__init__(statusCode, message)


class AlreadyExistUserException(CustomException):
    def __init__(self, message):
        statusCode = 402
        self.__message = message
        super().__init__(statusCode, message)


class AccessException(CustomException):
    def __init__(self, message):
        statusCode = 403
        self.__message = message
        super().__init__(statusCode, message)
