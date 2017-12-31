import datetime
import json
import os
import requests

import time

import mongoengine
from bson import json_util, ObjectId
from flask import Flask, request, Response
from flask_cors import CORS
from pymongo import MongoClient, errors


app = Flask(__name__)
CORS(app)

time.sleep(5)  # hack for the mongoDb database to get running




#user
@app.route("/user_service/<path:path>", methods=['GET'])
def get_user_service(path):
    response = requests.get('http://localhost:4444/containers/user_service').content
    user_services = json.loads(response)
    print(user_services)
    if user_services != None:
        for user_service in user_services:
            #load balance future implementation
            url = "http://"+user_service['host']+":"+user_service['port']+"/"+path
        serviceResponse = requests.post(url).content
        return Response(serviceResponse, status=200,
                        mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'User service not found!'}), status=404,
                        mimetype='application/json')


@app.route("/user_service/<path:path>", methods=['POST'])
def post_user_service(path):
    response = requests.get('http://localhost:4444/containers/user_service').content
    user_services = json.loads(response)
    if None != user_services:
        for user_service in user_services:
            #load balance future implementation
            url = "http://"+user_service['host']+":"+user_service['port']+"/"+path
        request_params = request.form
        serviceResponse = requests.post(url, data=request_params).content
        return Response(serviceResponse, status=200,
                        mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'User service not found!'}), status=404,
                        mimetype='application/json')





#booking
@app.route("/booking_service/<path:path>", methods=['GET'])
def get_booking_service(path):
    token = request.headers.get('authorization')
    response = requests.get('http://localhost:4444/containers/booking_service').content
    booking_services = json.loads(response)

    if None != booking_services:
        for booking_service in booking_services:
            #load balance future implementation
            url = "http://"+booking_service['host']+":"+booking_service['port']+"/"+path
        serviceResponse = requests.get(url, headers={'authorization':token}).content
        return Response(serviceResponse, status=200,
                        mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Booking service not found!'}), status=404,
                        mimetype='application/json')


@app.route("/booking_service/<path:path>", methods=['DELETE'])
def delete_booking_service(path):
    token = request.headers.get('authorization')
    response = requests.get('http://localhost:4444/containers/booking_service').content
    booking_services = json.loads(response)
    if None != booking_services:
        for booking_service in booking_services:
            # load balance future implementation
            url = "http://" + booking_service['host'] + ":" + booking_service['port'] + "/" + path
            serviceResponse = requests.delete(url, headers={'authorization': token})
        return Response(serviceResponse, status=200,
                        mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Booking service not found!'}), status=404,
                        mimetype='application/json')




@app.route("/booking_service/<path:path>", methods=['PUT', 'POST'])
def put_booking_service(path):
    token = request.headers.get('authorization')
    response = requests.get('http://localhost:4444/containers/booking_service').content
    booking_services = json.loads(response)

    if None != booking_services:
        for booking_service in booking_services:
            # load balance future implementation
            url = "http://" + booking_service['host'] + ":" + booking_service['port'] + "/" + path
            request_params = request.form
            serviceResponse = requests.put(url, data=request_params, headers={'authorization': token}).content
        return Response(serviceResponse, status=200,
                        mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Booking service not found!'}), status=404,
                        mimetype='application/json')






#room
@app.route("/room_service/<path:path>", methods=['GET'])
def get_room_service(path):
    token = request.headers.get('authorization')
    startTime = request.headers.get('startTime')
    endTime = request.headers.get('endTime')
    response = requests.get('http://localhost:4444/containers/room_service').content
    room_services = json.loads(response)

    if None != room_services:
        for room_service in room_services:
            # load balance future implementation
            url = "http://" + room_service['host'] + ":" + room_service['port'] + "/" + path
            serviceResponse = requests.get(url, headers={'authorization': token, 'startTime': startTime,
                                                         'endTime': endTime}).content
        return Response(serviceResponse, status=200,
                        mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Room service not found!'}), status=404,
                        mimetype='application/json')



@app.route("/room_service/<path:path>", methods=['PUT', 'POST'])
def put_room_service(path):
    token = request.headers.get('authorization')
    response = requests.get('http://localhost:4444/containers/room_service').content
    room_services = json.loads(response)

    if None != room_services:
        for room_service in room_services:
            # load balance future implementation
            url = "http://" + room_service['host'] + ":" + room_service['port'] + "/" + path
            request_params = request.form
            serviceResponse = requests.put(url, data=request_params, headers={'authorization': token}).content
        return Response(serviceResponse, status=200,
                        mimetype='application/json')
    else:
        return Response(json.dumps({'response': 'Room service not found!'}), status=404,
                        mimetype='application/json')






@app.route('/')
def hello_world():
    return 'Flask Dockerized'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5011))
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=port)
