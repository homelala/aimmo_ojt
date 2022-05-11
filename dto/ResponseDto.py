class ResponseDto:
    def __init__(self, statusCode, message, data=None):
        self.__statusCode = statusCode
        self.__message = message
        if data is None:
            self.__data = None
        else:
            self.__data = data

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data
