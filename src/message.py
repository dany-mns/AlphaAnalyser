import json


class Message:
    def __init__(self, jsonmes):
        self.dmessage = json.loads(jsonmes)
        self.from_user = self.dmessage["from"]
        self.body_message = self.dmessage["body"]
        self.timestamp = self.dmessage["timestamp"]
        self.type_message = self.dmessage["type"]

    def __str__(self):
        if self.type_message == "text":
            return f"from: [{self.from_user}], body: [{self.body_message}], type: [{self.type_message}]"
        else:
            return f"from: [{self.from_user}], body: [IMAGE], type: [{self.type_message}]"