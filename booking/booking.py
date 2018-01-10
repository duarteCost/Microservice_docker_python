import json
import os
import sys
import time
import pika
import socket

from bson import json_util, ObjectId
from flask import Flask, request, Response
from flask_cors import CORS
from pymongo import MongoClient, errors

# from communication.auth_client import AuthClient
#sys.path.insert(0, '../communication')
import auth_client

#server imports
import grpc
import sys
import time

with open('config.json', 'r') as f:
    config = json.load(f)

SELF_IP = config['DEFAULT']['SELF_IP']
RABBIT_HOST_IP = config['DEFAULT']['RABBIT_HOST_IP']
AUTH_IP = config['DEFAULT']['AUTH_IP']


class BookingRegister:
    def __init__(self, username="rabbituser", password="rabbituser", host=RABBIT_HOST_IP, port='5003'):
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, 5672, '/', self.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='queue', durable=True)
        #self.host = socket.gethostbyname(socket.gethostname())
        self.host = SELF_IP
        self.port = port

    def register(self):
        message = json_util.dumps({'host': self.host, 'service': 'booking_service', 'port': self.port,  'operation': 'register'})
        self.channel.basic_publish(exchange='',
                                   routing_key='queue',
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=2, ))
        print("[x] Sent %r " % message)
        # self.connection.close()

    def unregister(self):
        message = json_util.dumps({'host': self.host, 'service': 'booking_service', 'port': self.port, 'operation': 'unregister'})
        self.channel.basic_publish(exchange='',
                                   routing_key='queue',
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=2, ))
        print("[x] Sent %r " % message)
        # self.connection.close()


#end register

app = Flask(__name__)
CORS(app)
bookings = MongoClient('booking_mongo', 27017).bookingsDB.bookings

time.sleep(5)  # hack for the mongoDb database to get running

auth_client = auth_client.AuthClient(AUTH_IP, 50052)
booking_register = BookingRegister()
#booking class



#end booking class
@app.route('/')
def hello_world():
    return 'Hey from booking'


# insert booking
@app.route("/booking", methods=["PUT"])
def add_Booking():
    token = request.headers.get('authorization')
    payload = auth_client.rpc_run_read(token)
    error_message = 'Invalid token'
    if payload.value != error_message:
        request_params = request.form
        print(request_params);
        if 'startTime' not in request_params:
            return Response('A data e tempo de ínicio têm de ser definidas!', status=404, mimetype='application/json')
        elif 'endTime' not in request_params:
            return Response('A data e tempo de fim têm de ser definidas!', status=404, mimetype='application/json')
        elif 'roomId' not in request_params:
            return Response('O id da sala têm de ser definido!', status=404, mimetype='application/json')

        try:
            bookings.insert_one({
                'userId': payload.value,
                'roomId': request_params['roomId'],
                'startTime': request_params['startTime'],
                'endTime': request_params['endTime'],
                'description': request_params['description']
            })
        except errors.DuplicateKeyError as e:
            return Response('Marcação já existe!', status=404, mimetype='application/json')

        return Response('A marcação foi feita com sucesso', status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Para aceder esta rota é necessário um token válido!'}), status=404,
                        mimetype='application/json')


# uodate booking
@app.route("/booking/<string:bookingId>", methods=["POST"])
def update_booking(bookingId):
    token = request.headers.get('authorization')
    payload = auth_client.rpc_run_read(token)
    error_message = 'Invalid token'
    if payload.value != error_message:
        request_params = request.form
        if 'startTime' not in request_params:
            return Response('A data e tempo de ínicio têm de ser definidas!', status=404, mimetype='application/json')
        elif 'endTime' not in request_params:
            return Response('A data e tempo de fim têm de ser definidas!', status=404, mimetype='application/json')
        elif 'roomId' not in request_params:
            return Response('O id da sala têm de ser definido!', status=404, mimetype='application/json')

        set = {}
        set['userId'] = payload.value
        if 'startTime' in request_params:
            set['startTime'] = request_params['startTime']
        if 'endTime' in request_params:
            set['endTime'] = request_params['endTime']
        if 'roomId' in request_params:
            set['endTime'] = request_params['roomId']
        if 'description' in request_params:
            set['description'] = request_params['description']
        bookings.find_one_and_update({'_id': ObjectId(bookingId)}, {'$set': set})

        return Response('Atualizado com sucesso.', status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Para aceder esta rota é necessário um token válido!'}), status=404,
                        mimetype='application/json')


# gg
# find bookings of one user
@app.route("/bookings/currentUser", methods=["GET"])
def get_user_bookings():
    token = request.headers.get('authorization')
    payload = auth_client.rpc_run_read(token)
    error_message = 'Invalid token'
    if payload.value != error_message:
        booking = bookings.find({'userId': payload.value})
        if None == booking:
            return Response("Não foi encontrada nenhuma reserva com o id de utilizador:" + userId, status=404,
                            mimetype='application/json')
        return Response(json_util.dumps(booking), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Para aceder esta rota é necessário um token válido!'}), status=404,
                        mimetype='application/json')



# booking by id
@app.route("/booking/<string:bookingId>", methods=["GET"])
def get_booking_by_id(bookingId):
    token = request.headers.get('authorization')
    payload = auth_client.rpc_run_read(token)
    error_message = 'Invalid token'
    if payload.value != error_message:
        booking = bookings.find_one({'_id': ObjectId(bookingId)})
        if None == booking:
            return Response("Não foi encontrada nenhuma reserva com o id:" + bookingId, status=404,
                            mimetype='application/json')
        return Response(json_util.dumps(booking), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Para aceder esta rota é necessário um token válido!'}), status=404,
                        mimetype='application/json')


# all bookings
@app.route("/bookings", methods=['GET'])
def booking_list():
    token = request.headers.get('authorization')
    payload = auth_client.rpc_run_read(token)
    error_message = 'Invalid token'
    if payload.value != error_message:
        print(payload.value)
        booking = bookings.find({})
        if None == booking:
            return Response("Não foi encontrada nenhuma reserva", status=404,
                            mimetype='application/json')

        return Response(json_util.dumps(booking), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Para aceder esta rota é necessário um token válido!'}), status=404,
                        mimetype='application/json')


# delete booking by id
@app.route("/booking/<string:bookingId>", methods=["DELETE"])
def delete_booking(bookingId):
    token = request.headers.get('authorization')
    payload = auth_client.rpc_run_read(token)
    error_message = 'Invalid token'
    if payload.value != error_message:
        bookings.delete_one({'_id': ObjectId(bookingId)})
        return Response('Reserva eliminada com sucesso', status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Para aceder esta rota é necessário um token válido!'}), status=404,
                        mimetype='application/json')


if __name__ == "__main__":
    booking_register.register()
    port = int(os.environ.get('PORT', 5003))
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=port, use_reloader=False)
    booking_register.unregister()



