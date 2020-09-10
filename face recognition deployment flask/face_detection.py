import cv2
import numpy as mp
import matplotlib.pyplot as plt

face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
eye_cascade=cv2.CascadeClassifier('haarcascade_eye.xml')
def detect_face(img):
    face_img=img.copy()
    face_cord= face_cascade.detectMultiScale(face_img,scaleFactor=1.2,minNeighbors=5) #x,y,width,height returned
    for (x,y,w,h) in face_cord:
        cv2.rectangle(face_img,(x,y),(x+w,y+h),(255,255,255),10)
    return face_img

def detect_eye(img):
    face_img=img.copy()
    eye_cord= eye_cascade.detectMultiScale(face_img,scaleFactor=1.2,minNeighbors=5) #x,y,width,height returned
    for (x,y,w,h) in eye_cord:
        cv2.rectangle(face_img,(x,y),(x+w,y+h),(255,255,255),10)
    return face_img
        
def detect_eye_and_face(img):
    face_img=img.copy()
    face_cord= face_cascade.detectMultiScale(face_img,scaleFactor=1.2,minNeighbors=5) #x,y,width,height returned
    for (x,y,w,h) in face_cord:
        cv2.rectangle(face_img,(x,y),(x+w,y+h),(255,255,255),10)

    face_img2=img.copy()
    eye_cord= eye_cascade.detectMultiScale(face_img2,scaleFactor=1.2,minNeighbors=5) #x,y,width,height returned
    for (x,y,w,h) in eye_cord:
        cv2.rectangle(face_img,(x,y),(x+w,y+h),(255,255,255),10)
    return face_img
        
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read(0)
    frame=detect_eye_and_face(frame)
    cv2.imshow('video face detect',frame)
    k=cv2.waitKey(1)
    if k==27:
        break

cap.release()
cv2.destroyAllWindows()

    
    
