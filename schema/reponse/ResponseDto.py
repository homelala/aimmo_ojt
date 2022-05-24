import json


class ResponseDto:
    def __init__(self, statusCode, message, data=None):
        self.statusCode = statusCode
        self.message = message
        if data is not None:
            self.data = data
