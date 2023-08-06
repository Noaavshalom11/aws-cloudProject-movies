#!flask/bin/python
import json
from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun
from flask_cors import CORS
import boto3
import requests
import uuid
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import simplejson as json 



application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}}) 

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


# ADD JOB

@application.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('users')
    table.put_item(Item=data)
    
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
# TEST -
# curl -i -X POST -H "Content-Type: application/json" -d '{"user_id": "xxxxxxxxxxxxxxx"}' http://localhost:8000/add_user


# upload and analyze profile image
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
    
    try:
        confidence = response['FaceDetails'][0]['Confidence'];
        return {"img_url": img_url, "confidence": confidence}
        
    except:
        return {"img_url": img_url, "confidence": "no_match"}
    

@application.route('/get_user', methods=['POST'])
def get_user():
    data = request.data
    data_json = json.loads(data)
    user_id = data_json['user_id']

    print(user_id)

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('users')
    respponse = table.get_item(Key={
            'user_id': user_id,
    })
    
    print(respponse)

    
    img_url = respponse['Item']['img_url']
    user_name = respponse['Item']['user_name']


    return Response(json.dumps({"img_url": img_url, "user_name": user_name}), mimetype='application/json', status=200)


@application.route('/add_review', methods=['POST'])
def add_review():
    data = request.get_json()
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('reviews')
    review_id = (str(uuid.uuid4()))
    data['review_id'] = review_id
    print(data)
    table.put_item(Item=data)
    
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
# TEST -
# curl -i -X POST -H "Content-Type: application/json" -d '{"user_id": "xxxxxxxxxxxxxxx"}' http://localhost:8000/add_review

# GET REVIEWS BY ID

@application.route('/get_reviews_by_id', methods=['POST'])
def get_reviews_by_id():
    data = request.data
    data_json = json.loads(data)
    imdb_id = data_json['imdb_id']
    print(imdb_id)

    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('reviews')
    print(table)

    respponse = table.scan(FilterExpression=Attr("imdb_id").eq(imdb_id))

    print(respponse)

    

    return Response(json.dumps(respponse['Items']), mimetype='application/json', status=200)    
    
# curl -i -X POST -H "Content-Type: application/json" -d '{"imdb_id": "tt10648342"}' http://localhost:8000/get_reviews_by_id


@application.route('/add_movie_data', methods=['POST'])
def add_movie_data():
    data = request.get_json()
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('reviews')
    movie_id  = (str(uuid.uuid4()))
    data['movie_id'] = movie_id
    print(data)
    table.put_item(Item=data)
    
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
# TEST -
# curl -i -X POST -H "Content-Type: application/json" -d '{"user_id": "xxxxxxxxxxxxxxx"}' http://localhost:8000/add_review


if __name__ == '__main__':
    flaskrun(application)