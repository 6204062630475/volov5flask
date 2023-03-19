from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2
#--------------------------------

from server import create_user
#--------------------------------

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def button():
    print("ทำงาน")
    create_user(geta(VideoCamera()))
    return render_template('index.html')

def gen(camera):
    while True:
        frame,A = camera.get_frame()
        #showa(A)
        print("อันนี้ a ",A)
        
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def geta(camera):
    while True:
        frame,A = camera.get_frame()
        return A

# class showa():
#     def showa(z):
#         print("showa",z)
#         return z

@app.route('/video_feed')
def video_feed():
    # GenVideoCamera,AVideoCamera = gen(VideoCamera())
    # create_user(AVideoCamera)
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    

if __name__ == '__main__':
    app.run(port=5000, debug=False)
###############################
#-----------------------------
