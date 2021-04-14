import json


class Message:
    def __init__(self, jsonmes):
        self.dmessage = json.loads(jsonmes)
        self.from_user = self.dmessage["from"]
        self.body_message = self.dmessage["body"]
        self.timestamp = self.dmessage["timestamp"]
        self.type_message = self.dmessage["type"]