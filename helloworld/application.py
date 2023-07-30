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
    bucket = 'jce-cloud-project'
    img = request.files['img']
    s3 = boto3.resource('s3', region_name='us-east-1')
    img_path  = "images/%s.jpg" %  (str(uuid.uuid4()))
    s3.Bucket(bucket).upload_fileobj(img, img_path, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'}) 
    img_url = 'https://jce-cloud-project.s3.amazonaws.com/'+ img_path
    
    
    rekognition = boto3.client("rekognition", region_name = 'us-east-1')
    
    key = img_path

    response = rekognition.detect_faces(
    Image={
        'S3Object': {
            'Bucket': bucket,
            'Name': key,
        }
    }
    )
    
    
    print(response['FaceDetails'][0]['Confidence'])
    confidence = response['FaceDetails'][0]['Confidence'];
    sharpness = response['FaceDetails'][0]['Quality']['Sharpness'];


    return {"img_url": img_url, "confidence": confidence, "sharpness": sharpness}
    


if __name__ == '__main__':
    flaskrun(application)