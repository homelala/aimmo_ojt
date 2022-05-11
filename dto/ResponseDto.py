import json


class ResponseDto:
    def __init__(self, statusCode, message, data=None):
        self.statusCode = statusCode
        self.message = message
        if data is None:
            self.data = None
        else:
            self.data = data

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))
