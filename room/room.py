import datetime
import json
import os
import requests
import pika
import socket
import time

import mongoengine
from bson import json_util, ObjectId
from flask import Flask, request, Response
from flask_cors import CORS
from pymongo import MongoClient, errors

import auth_client
from room_model import Room

with open('config.json', 'r') as f:
    config = json.load(f)

SELF_HOST_IP = config['DEFAULT']['SELF_HOST_IP']
RABBIT_HOST_IP = config['DEFAULT']['RABBIT_HOST_IP']
AUTH_HOST_IP = config['DEFAULT']['AUTH_HOST_IP']
BOOKING_HOST_IP = config['DEFAULT']['BOOKING_HOST_IP']

#register

class RoomRegister:
    def __init__(self, username="rabbituser", password="rabbituser", host=RABBIT_HOST_IP, port='5004'):
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, 5672, '/', self.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='queue', durable=True)
        #self.host = socket.gethostbyname(socket.gethostname())
        self.host = SELF_HOST_IP
        self.port = port

    def register(self):
        message = json_util.dumps({'host': self.host, 'service': 'room_service', 'port': self.port, 'operation': 'register'})
        self.channel.basic_publish(exchange='',
                                   routing_key='queue',
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=2, ))
        print("[x] Sent %r " % message)
        # self.connection.close()

    def unregister(self):
        message = json_util.dumps({'host': self.host, 'service': 'room_service', 'port': self.port, 'operation': 'unregister'})
        self.channel.basic_publish(exchange='',
                                   routing_key='queue',
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=2, ))
        print("[x] Sent %r " % message)
        # self.connection.close()

#end register

app = Flask(__name__)
CORS(app)
rooms = MongoClient('room_mongo', 27017).roomsDB.room
#rooms = MongoClient('localhost', 27017).roomsDB.room

time.sleep(5)  # hack for the mongoDb database to get running


auth_client = auth_client.AuthClient(AUTH_HOST_IP, 50052)
room_register = RoomRegister()


@app.route("/rooms/floor/<string:floor>", methods=["GET"])
def get_room_by_floor(floor):
    token = request.headers.get('authorization')
    payload = auth_client.rpc_run_read(token)
    error_message = 'Invalid token'
    if payload.value != error_message:
        response =  requests.get('http://'+BOOKING_HOST_IP+':5003/bookings', headers={'authorization':token}).content
        startTime = request.headers.get('startTime')
        endTime = request.headers.get('endTime')
        timestamp_startTime = time.mktime(datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M").timetuple())
        timestamp_endTime = time.mktime(datetime.datetime.strptime(endTime, "%Y-%m-%dT%H:%M").timetuple())

        bookingsJSON = json.loads(response)
        print("heeloo")
        availableRooms = []
        rooms_by_floor = rooms.find({'floor': int(floor)})
        for room in rooms_by_floor:
            availableRooms.append(room)
        #return Response(response, status=200, mimetype='application/json')
        for booking in bookingsJSON:
            print(booking)
            o_timestamp_startTime = time.mktime(
                datetime.datetime.strptime(str(booking['startTime']), '%Y-%m-%dT%H:%M').timetuple())
            o_timestamp_endTime = time.mktime(
                datetime.datetime.strptime(str(booking['endTime']), '%Y-%m-%dT%H:%M').timetuple())
            time_range = range(int(o_timestamp_startTime), int(o_timestamp_endTime), 1)
            if int(timestamp_startTime in time_range or int(timestamp_endTime) in time_range):
                print(booking)
                rooms_by_floor = rooms.find({'floor': int(floor)})
                for room in rooms_by_floor:
                    room_id = str(room['_id'])
                    if room_id == booking['roomId']:
                        availableRooms.remove(room)
                        print(room)

        return Response(json_util.dumps(availableRooms), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Para aceder esta rota é necessário um token válido!'}), status=404,
                        mimetype='application/json')



# insert room
@app.route("/rooms", methods=["PUT"])
def add_room():
    token = request.headers.get('authorization')
    payload = auth_client.rpc_run_read(token)
    error_message = 'Invalid token'
    if payload.value != error_message:
        request_params = request.form
        print(request_params);
        if 'floor' not in request_params:
            return Response('O andar tem de ser definidas!', status=404, mimetype='application/json')
        elif 'number' not in request_params:
            return Response('O número da sala tem de ser definido!', status=404, mimetype='application/json')

        floor = request_params['floor']
        number = request_params['number']
        description = request_params['description']
        mongoengine.connect(db='roomsDB', host='room_mongo', port=27017)

        try:
            Room(id=ObjectId(), floor=floor, number=number, description=description).save()
            return Response(json.dumps({'response': 'Successful operation'}), status=200, mimetype='application/json')
        except errors.DuplicateKeyError as e:
            return Response('Sala ja exite já existe!', status=404, mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Para aceder esta rota é necessário um token válido!'}), status=404,
                        mimetype='application/json')


# room by id
@app.route("/rooms/<string:roomId>", methods=["GET"])
def get_room(roomId):
    token = request.headers.get('authorization')
    payload = auth_client.rpc_run_read(token)
    error_message = 'Invalid token'
    if payload.value != error_message:
        room = rooms.find_one({'_id': ObjectId(roomId)})
        if None == room:
            return Response("Não foi encontrada nenhuma sala com o id de sala:" + roomId, status=404,
                            mimetype='application/json')

        return Response(json_util.dumps(room), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Para aceder esta rota é necessário um token válido!'}), status=404,
                        mimetype='application/json')




# all rooms
@app.route("/rooms", methods=['GET'])
def rooms_list():
    token = request.headers.get('authorization')
    payload = auth_client.rpc_run_read(token)
    error_message = 'Invalid token'
    if payload.value != error_message:
        room = rooms.find({})
        if None == room:
            return Response("Não foi encontrada nenhuma sala", status=404,
                            mimetype='application/json')

        return Response(json_util.dumps(room), status=200, mimetype='application/json')

    else:
        return Response(json.dumps({'response': 'Para aceder esta rota é necessário um token válido!'}), status=404,
                        mimetype='application/json')


# delete by id
@app.route("/rooms/<string:roomId>", methods=["DELETE"])
def delete_room(roomId):
    token = request.headers.get('authorization')
    payload = auth_client.rpc_run_read(token)
    error_message = 'Invalid token'
    if payload.value != error_message:
        rooms.delete_one({'_id': ObjectId(roomId)})
        return Response('Sala eliminada com sucesso', status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Para aceder esta rota é necessário um token válido!'}), status=404,
                        mimetype='application/json')

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

if __name__ == "__main__":
    room_register.register()
    port = int(os.environ.get('PORT', 5004))
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=port, use_reloader=False)
    room_register.unregister()
