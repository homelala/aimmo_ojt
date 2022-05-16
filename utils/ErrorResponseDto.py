import json


class ErrorResponseDto(Exception):
    def __init__(self, message, statusCode=400):
        Exception.__init__(self, message)
        self.message = message
        self.statusCode = statusCode
