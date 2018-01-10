import datetime
import jwt

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 120



class AuthService:
    # Receives the user id when a login is made and generates a authentication token based on user_id and expiration.
    def create_auth_token(user_id):
        payload = {
            'user_id': str(user_id),
            'expiration': str(datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS))
        }
        auth_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        print(str(auth_token))
        return auth_token.decode('utf-8')

    # Receives the authentication token. If token is valid or is not expired, the user_id is returned.
    def read_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, JWT_SECRET, algorithm=JWT_ALGORITHM)
            print(str(payload['user_id']))
            return payload['user_id']
        except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            print('Invalid token')
            return 'Invalid token'
