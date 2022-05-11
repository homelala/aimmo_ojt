import json


class ErrorResponseDto:
    def __init__(self, message, statusCode):
        self.message = message
        self.statusCode = statusCode

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))
