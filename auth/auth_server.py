# Starts the server to receive rpc requests
import socket
import time
from concurrent import futures

import auth_pb2
import auth_pb2_grpc
import grpc
import pika
import json

from auth import AuthService


with open('config.json', 'r') as f:
    config = json.load(f)

SELF_IP = config['DEFAULT']['SELF_IP']
RABBIT_HOST_IP = config['DEFAULT']['RABBIT_HOST_IP']


class AuthServicer(auth_pb2_grpc.AuthServicer):
    def read_auth_token(self, request, context):
        response = auth_pb2.AuthToken()  # message expected = AuthToken --see auth.proto
        response.value = AuthService.read_auth_token(
            request.value)  # rpc call to get token and assign to AuthToken.value
        return response

    def create_auth_token(self, request, context):
        response = auth_pb2.UserId()  # message expected
        response.value = AuthService.create_auth_token(
            request.value)  # rpc call to validate token and get user_id; assigns to UserId.value
        return response


class AuthRegister:
    def __init__(self, username="rabbituser", password="rabbituser", host=RABBIT_HOST_IP, port='50052'):
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, 5672, '/', self.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='queue', durable=True)
        #self.host = socket.gethostbyname(socket.gethostname())
        self.host = SELF_IP
        self.port = port

    def register(self):
        message = json.dumps({'host': self.host, 'service': 'auth_service', 'port': self.port, 'operation': 'register'})
        self.channel.basic_publish(exchange='',
                                   routing_key='queue',
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=2, ))
        print("[x] Sent %r " % message)
        # self.connection.close()

    def unregister(self):
        message = json.dumps({'host': self.host, 'service': 'auth_service', 'port': self.port, 'operation': 'unregister'})
        self.channel.basic_publish(exchange='',
                                   routing_key='queue',
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=2, ))
        print("[x] Sent %r " % message)
        # self.connection.close()


auth_register = AuthRegister()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServicer_to_server(AuthServicer(), server)
    print('Starting server. Listening on port 50052')
    server.add_insecure_port('[::]:50052')
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    auth_register.register()
    serve()
    auth_register.unregister()
