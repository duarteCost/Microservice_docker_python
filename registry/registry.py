import threading
import json
import mongoengine
import os
import pika
import time

from bson import ObjectId, json_util
from flask import Flask, json, Response
from flask_cors import CORS
from pymongo import MongoClient, errors

from registry_model import Registry

with open('config.json', 'r') as f:
    config = json.load(f)

RABBIT_HOST_IP = config['DEFAULT']['RABBIT_HOST_IP']

def callback(ch, method, properties, body):
    print("[x] Received %r " % body)
    # time.sleep(body.count(b'.'))
    obj = json.loads(body)
    host = obj["host"]
    service = obj["service"]
    port = obj["port"]
    status = obj["operation"]
    if status == "register":
        registry_create(service=service, host=host, service_port=port)
    else:
        registry_delete(service=service, host=host, service_port=port)
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


class RegistryListener:
    def __init__(self, username="rabbituser", password="rabbituser", host=RABBIT_HOST_IP):
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, 5672, '/', self.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='queue', durable=True)
        print("[*] Working for messages. Exit with CTRL+C.")

    def consume(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(callback, queue='queue', no_ack=False)
        self.channel.start_consuming()


app = Flask(__name__)
CORS(app)
mongodb = MongoClient('registry_mongo', 27017).registrydb.registry
time.sleep(5)


@app.route('/containers', methods=['POST'])
def registry_create(service, host, service_port):
    try:
        mongoengine.connect(db='registrydb', host='registry_mongo', port=27017)
        Registry(ObjectId(), service, host, str(service_port)).save()
        print('Start saving document...')
        return Response(json_util.dumps({'response': 'Successful operation'}), status=200,
                        mimetype='application/json')
    except (errors.DuplicateKeyError, mongoengine.errors.NotUniqueError, errors.ServerSelectionTimeoutError):
        print('Stop saving document...')
        return Response(json_util.dumps({'response': 'Error'}),
                        status=500, mimetype='application/json')


     
@app.route('/containers', methods=['DELETE'])
def registry_delete(service, host, service_port):
    try:
        registry = mongodb.find({'service': service, 'host': host, 'port': str(service_port)})
        if registry is None:
            print('Stop deleting document...')
            return Response(json_util.dumps({'response': 'No registry found'}),
                            status=500, mimetype='application/json')
        else:
            print('Start deleting document...')
            mongodb.remove({'service': service, 'host': host, 'port': str(service_port)})
            return Response(json_util.dumps({'response': 'Successful operation'}), status=200,
                            mimetype='application/json')
    except errors.ServerSelectionTimeoutError:
        return False


@app.route('/containers/{name}', methods=['GET'])
def get_registry(service):
    try:
        registries = mongodb.find({'service': service})
        if registries is None:
            return Response(json_util.dumps({'response': 'No container found'}),
                            status=500, mimetype='application/json')
        else:
            return Response(json_util.dumps(registries), status=200,
                            mimetype='application/json')
    except errors.ServerSelectionTimeoutError:
        return Response(json_util.dumps({'response': 'Mongodb is not running'}), status=500,
                        mimetype='application/json')


@app.route("/containers/auth_service", methods=['GET'])
def get_auth_service():
    container = mongodb.find({'service': 'auth_service'})
    if container is None:
        return Response("No service", status=404,
                        mimetype='application/json')

    return Response(json_util.dumps(container), status=200, mimetype='application/json')


@app.route("/containers/user_service", methods=['GET'])
def get_user_service():
    container = mongodb.find({'service': 'user_service'})
    if container is None:
        return Response("No registry found", status=404,
                        mimetype='application/json')

    return Response(json_util.dumps(container), status=200, mimetype='application/json')


@app.route("/containers/booking_service", methods=['GET'])
def get_booking_service():
    container = mongodb.find({'service': 'booking_service'})
    if container is None:
        return Response("No container found", status=404,
                        mimetype='application/json')

    return Response(json_util.dumps(container), status=200, mimetype='application/json')


@app.route("/containers/room_service", methods=['GET'])
def get_room_service():
    container = mongodb.find({'service': 'room_service'})
    if container is None:
        return Response("No container found", status=404,
                        mimetype='application/json')

    return Response(json_util.dumps(container), status=200, mimetype='application/json')


@app.route('/containers/all', methods=['GET'])
def get_containers():
    try:
        containers = mongodb.find({})
        if containers is None:
            return Response(json_util.dumps({'response': 'No registry found'}),
                            status=500, mimetype='application/json')
        else:
            return Response(json_util.dumps(containers), status=200,
                            mimetype='application/json')
    except errors.ServerSelectionTimeoutError:
        return Response(json_util.dumps({'response': 'Mongodb is not running'}), status=500,
                        mimetype='application/json')


def run_listener():
    print('Run listener')
    registry = RegistryListener()
    registry.consume()


thread = threading.Thread(target=run_listener)
thread.start()

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 4444))
        app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("[*] Terminate.")
