import grpc

import auth_pb2_grpc, auth_pb2


class AuthClient:
    def __init__(self, host='localhost', port=50052):
        conn_str = '{}:{}'.format(host, port)
        self.channel = grpc.insecure_channel(conn_str)
        self.stub = auth_pb2_grpc.AuthStub(self.channel)

    # Login call this method
    def rpc_run_create(self, id):
        print('grpc')
        user_id = auth_pb2.AuthToken(value=str(id))
        response = self.stub.create_auth_token(user_id)
        return response

    def rpc_run_read(self, auth_token):
        token = auth_pb2.UserId(value=str(auth_token))
        response = self.stub.read_auth_token(token)
        return response
