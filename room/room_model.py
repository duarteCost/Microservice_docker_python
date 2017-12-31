from mongoengine import *


class Room(Document):
    id = ObjectIdField(required=True, primary_key=True)
    floor = IntField(max_length=100, required=True)
    number = IntField(max_length=100, required=True)
    description = StringField(max_length=200, required=True)