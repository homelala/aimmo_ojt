import json


class ResponseDto:
    def __init__(self, data=None):
        if data is not None:
            self.data = data
