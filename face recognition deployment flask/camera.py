# import the necessary packages
import cv2
import os
import numpy as np
from PIL import Image
import sqlite3 

path='dataset'
# defining face detector
# face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('train_dataset/trainer.yml')
cascadePath = "haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
ds_factor=0.6


path='dataset'
def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        
        print(Id)
        faces.append(imageNp)
        Ids.append(Id)
        
        
    return faces,Ids
class VideoCamera(object):
    def __init__(self):
       #capturing video
       self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        #releasing camera
        self.video.release()
    def get_frame(self):
       #extracting frames
        conn=sqlite3.connect("user.db")
        ret, frame = self.video.read()
        #--------------------------------------------------------------frame shouldnt be empty-----------------------------------------
        cv2.waitKey(1)
        frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor,
        interpolation=cv2.INTER_AREA)                    
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.3,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            cmd="select f_name from user where id="+str(Id)
            cursor=conn.execute(cmd)
            data=cursor.fetchall()
            # print(data[0])
            Id="Unknown"
            if data:
                Id=data[0][0]
            
            # if(Id==1):
            #     Id="Gokul"
            # elif(Id==2):
            #     Id="Sudha"
            # else:
            #     Id="Unknown"
            cv2.putText(frame,str(Id), (x,y-10),font,1,(0,255,0),2,cv2.LINE_AA)

        # face_rects=face_cascade.detectMultiScale(gray,1.3,5)
        # for (x,y,w,h) in face_rects:
        #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            
        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


    def create(self,id,num):

        ret, frame = self.video.read()
        frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor,
        interpolation=cv2.INTER_AREA)                    
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        face_cord=faceCascade.detectMultiScale(gray, 1.3,5)
        for (x,y,w,h) in face_cord:
            cv2.imwrite("dataset/user."+str(id)+"."+str(num)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()












    def train():

        faces,Ids = getImagesAndLabels('dataSet')
        recognizer.train(faces, np.array(Ids))
        recognizer.save('train_dataset/trainer.yml')

