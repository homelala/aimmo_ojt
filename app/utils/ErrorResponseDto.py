import json


class ErrorResponseDto(Exception):
    def __init__(self, message, statusCode):
        Exception.__init__(self, message)
        self.message = message
        self.statusCode = statusCode
