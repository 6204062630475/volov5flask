from flask import Flask, render_template, Response, request, jsonify
from camera import VideoCamera
import cv2
from server import create_count
from pymongo import MongoClient
from flask_pymongo import PyMongo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
app = Flask(__name__)
#-----------------------

client = MongoClient('mongodb://localhost:27017/')
db = client['historycount']
collection = db['count']


app.config['MONGO_URI'] = 'mongodb://localhost:27017/historycount'
mongo = PyMongo(app)

#-----------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def button():
    #print("ทำงาน")
    create_count(geta(VideoCamera()))
    data = []
    for doc in mongo.db.count.find():
        data.append({
            'count': doc['count'],
            'Date': doc['Date'],
        })
    return render_template('index.html', data=data)

def gen(camera):
    while True:
        frame,A = camera.get_frame()
        #print("อันนี้ a ",get_count())
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def geta(camera):
    while True:
        frame,A = camera.get_frame()
        return A


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/history')
def history():
    
    num = int(request.args.get('num', 5))
    if num == -1:
        cursor = collection.find().sort('timestamp', -1)
    else:
        cursor = collection.find().sort('timestamp', -1).limit(num)
    data = []
    for doc in cursor:
        data.append({
            'count': doc['count'],
            'Date': doc['Date'],
        })
    average = get_average()
    #print("indexทำงาน ",data)
    return render_template('history.html', data=data, num=num, average=average)

def get_average():
    data = list(collection.find({}, {'_id': 0, 'count': 1}))
    counts = [d['count'] for d in data]
    average = sum(counts) / len(counts)
    return average  

if __name__ == '__main__':
    app.run(port=5000, debug=False)

#-----------------------------
