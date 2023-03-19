import cv2
import torch
import numpy as np        
        
model = torch.hub.load('ultralytics/yolov5', 'custom',path='best.pt',force_reload=True)
#area=[(237,14),(200,576),(869, 582),(874, 13)]
area=[(80,15),(80,458),(600,458),(600,15)]
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # self.video = cv2.resize(self.video,(1020,600))
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        results=model(image)
        # a=np.squeeze(results.render())
        list=[]
        for index, row in results.pandas().xyxy[0].iterrows():
            x1 = int(row['xmin'])
            y1 = int(row['ymin'])
            x2 = int(row['xmax'])
            y2 = int(row['ymax'])
            d=(row['name'])
            cx=int(x1+x2)//2
            cy=int(y1+y2)//2
            if 'fish' in d:
                results=cv2.pointPolygonTest(np.array(area,np.int32),((cx,cy)),False)
                if results >= 0:
                    # print(d)                
                    cv2.rectangle(image,(x1,y1),(x2,y2),(0,0,255),3)
                    cv2.putText(image,str(d),(x1,y1),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
                    list.append([cx])
        cv2.polylines(image,[np.array(area,np.int32)],True,(0,255,0),2)
        a=(len(list))
        print(a)
        cv2.putText(image,str(a),(15,30),cv2.FONT_HERSHEY_PLAIN,2,(255,255,0),2)

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes(),a