from flask import Flask, Response
import pymongo
import json
from bson.objectid import ObjectId
from camera import VideoCamera
from datetime import datetime
app = Flask(__name__)
try:
    mongo = pymongo.MongoClient(
        # host="localhost",
        # port=27017,
        # serverSelectionTimeoutMS= 1000

        "mongodb+srv://fishdb:fishdb@cluster0.6jeeb1j.mongodb.net/?retryWrites=true&w=majority"
    )
    db = mongo.historycount  
    mongo.server_info()
except:
    print("Error Cannot connect to db")
#-------------------------------------------
# @app.route('/count', methods=['GET'])
# def get_count():
#     try:
#         data = list(db.count.find())
#         for user in data:
#             user["_id"] = str(user["_id"])
#         return Response(
#             response = json.dumps(data),
#             status=500,
#             mimetype="application/json"
#         )
#     except Exception as ex:
#         print(ex)
#         return Response(response = json.dumps({"message":"cannot read"}),status=500,mimetype="application/json")
#-------------------------------------------
def create_count(a):
    now = datetime.now()
    #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    try:
        user = {"count":a,"Date":now}
        dbResponse = db.count.insert_one(user)
        print(dbResponse.inserted_id)
        return Response(
            response = json.dumps({"count":"10",
                        "id":f"{dbResponse.inserted_id}"
                        }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
#-------------------------------------------
def gen(camera):
    while True:
        frame,A = camera.get_frame()
        print("อันนี้ a ",A)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'),A
#-------------------------------------------
if __name__ == '__main__':
    app.run(port=80, debug=True)