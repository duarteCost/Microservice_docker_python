from mongoengine import *


class Registry(Document):
    id = ObjectIdField(required=True, primary_key=True)
    service = StringField(max_length=200, required=True)
    host = StringField(max_length=200, required=True)
    port = StringField(max_length=200, required=True)

    def __init__(self, user_id, service, host, port, *args, **values):
        super().__init__(*args, **values)
        self.id = user_id
        self.service = service
        self.host = host
        self.port = port
