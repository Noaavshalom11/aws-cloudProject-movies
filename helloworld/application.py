#!flask/bin/python
import json
from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun
from flask_cors import CORS
import boto3
import requests
import uuid

application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}}) 

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)



@application.route('/upload_image', methods=['POST'])
def upload_image():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    


if __name__ == '__main__':
    flaskrun(application)