import os
import time
import socket

import mongoengine
import pika

from auth_client import AuthClient
from bson import ObjectId, json_util
from flask import Flask, request, Response
from flask_cors import CORS
from pymongo import MongoClient, errors
from user_model import User
from werkzeug.security import check_password_hash


class UserRegister:
    def __init__(self, username="rabbituser", password="rabbituser", host='192.168.1.6', port='5000'):
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, 5672, '/', self.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='queue', durable=True)
        #self.host = socket.gethostbyname(socket.gethostname())
        self.host = '192.168.1.6'
        self.port = port

    def register(self):
        message = json_util.dumps({'host': self.host, 'service': 'user_service', 'port': self.port, 'operation': 'register'})
        self.channel.basic_publish(exchange='',
                                   routing_key='queue',
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=2, ))
        print("[x] Sent %r " % message)
        # self.connection.close()

    def unregister(self):
        message = json_util.dumps({'host': self.host, 'service': 'user_service', 'port': self.port, 'operation': 'unregister'})
        self.channel.basic_publish(exchange='',
                                   routing_key='queue',
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=2, ))
        print("[x] Sent %r " % message)
        #self.connection.close()


app = Flask(__name__)
CORS(app)
mongodb = MongoClient('user_mongo', 27017).userdb.user
time.sleep(5)

auth_client = AuthClient('auth_service', 50052)
user_register = UserRegister()


@app.route('/user/register', methods=['POST'])
# Handler for HTTP Post - "/user/register"
def create_user():
    request_params = request.form
    print(request_params)
    if 'name' not in request_params:
        return Response(json_util.dumps({'response': 'Missing parameter: name'}), status=404,
                        mimetype='application/json')
    elif 'surname' not in request_params:
        return Response(json_util.dumps({'response': 'Missing parameter: surname'}), status=404,
                        mimetype='application/json')
    elif 'email' not in request_params:
        return Response(json_util.dumps({'response': 'Missing parameter: email'}), status=404,
                        mimetype='application/json')
    elif 'password' not in request_params:
        return Response(json_util.dumps({'response': 'Missing parameter: password'}), status=404,
                        mimetype='application/json')
    elif 'confirm-password' not in request_params:
        return Response(json_util.dumps({'response': 'Missing parameter: confirm password'}), status=404,
                        mimetype='application/json')

    name = request_params['name']
    surname = request_params['surname']
    password = request_params['password']
    email = request_params['email']
    role = email.split("@")[1].split(".")[0]

    try:
        mongoengine.connect(db='userdb', host='user_mongo', port=27017)
        User(ObjectId(), email, password, role, name, surname).save()
        return Response(json_util.dumps({'response': 'Successful operation'}),
                        status=200, mimetype='application/json')
    except (errors.DuplicateKeyError, mongoengine.errors.NotUniqueError):
        return Response(json_util.dumps({'response': 'User already exists'}),
                        status=404, mimetype='application/json')
    except errors.ServerSelectionTimeoutError:
        return Response(json_util.dumps({'response': 'Mongodb is not running'}), status=500,
                        mimetype='application/json')


@app.route('/user/all', methods=['GET'])
# Handler for HTTP GET - "/user/all"
def get_user():
    try:
        users = mongodb.find({})
        if users is None:
            return Response(json_util.dumps({'response': 'No users found'}),
                            status=500, mimetype='application/json')
        else:
            return Response(json_util.dumps(users), status=200,
                            mimetype='application/json')
    except errors.ServerSelectionTimeoutError:
        return Response(json_util.dumps({'response': 'Mongodb is not running'}), status=500,
                        mimetype='application/json')


@app.route('/user/login', methods=['POST'])
# Handler for HTTP POST - "/user/login"
def login_user():
    request_params = request.form
    print(request_params)
    if 'email' not in request_params:
        return Response(json_util.dumps({'response': 'Missing parameter: email'}), status=404, mimetype='application'
                                                                                                        '/json')
    elif 'password' not in request_params:
        return Response(json_util.dumps({'response': 'Missing parameter: password'}), status=404,
                        mimetype='application/json')

    password = request_params['password']
    email = request_params['email']

    existing_user = mongodb.find_one({'email': email})
    if existing_user is None and check_password_hash(existing_user['password'], password):
        return Response(json_util.dumps({'response': 'Invalid username/password supplied'}), status=404,
                        mimetype='application/json')
    # RPC communication to generate token when user does the login
    auth_token = auth_client.rpc_run_create(existing_user['_id'])
    print(auth_token.value)
    return Response(json_util.dumps({'response': 'Successful operation', 'token': str(auth_token.value)}), status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    user_register.register()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
    user_register.unregister()
