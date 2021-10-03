from PIL import Image as IM
from PIL import ImageTk
from tkinter import *
from tkinter import StringVar
import threading
import imutils
import cv2
import numpy as np
import pandas as pd

class Detector:
    def __init__(self,vs,classifier,standalone_flag=0):
        self.flag = standalone_flag;
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stop = None
        self.faceDetector = cv2.CascadeClassifier(classifier)
        self.result = []
    def init_thread(self, panel=None, window=None):
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop,args=[panel,window])
        self.thread.start()
    def videoLoop(self,panel,window):
        try:
            while(not self.stop.isSet()):
                ret,self.frame = self.vs.read()
                if self.frame is not None:
                    img = None
                    img = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
                    if self.flag == 1:
                        img = self.detectFace(img)
                    if window:
                        img = IM.fromarray(img)
                        img=ImageTk.PhotoImage(img)
                        if(panel is None):
                            panel = Label(window, image=img)
                            panel.image=img
                            panel.pack(side='left',padx=10,pady=10)
                        else:
                            panel.configure(image=img)
                            panel.image=img
                    else:
                        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
                        cv2.imshow('Video',img)
                        if cv2.waitKey(1) & 0xFF ==ord('q'):
                            self.onClose()
        except RuntimeError:
            print("Some Thing went wrong")
    def still_photo(self,img_file=None):
        ret,self.frame = self.vs.read(img_file)
        self.frame = imutils.resize(self.frame,width=400)

        img=cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
        if(self.flag==0):
            img = self.detectFace(img)
        
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            cv2.imshow('Video',img)
        self.onClose()
    def detectFace(self,frame):
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = self.faceDetector.detectMultiScale(gray,1.3,4)
        for(x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            bbox = gray[x:x+w,y:y+h]
            points = cv2.goodFeaturesToTrack(bbox,30,0.1,10)
            if points is not None:
                if len(points)>0:
                    points = np.int0(points)
                    self.result.append(points)
                    for p in points:
                        a,b = p.ravel()
                        cv2.circle(frame,(a+x,b+y),2,(0,0,255),-1)
        return frame
    def get_result(self):
        return self.result
    def onClose(self):
        if self.stop:
            self.stop.set()
        if self.vs:
            self.vs.release()
        cv2.destroyAllWindows()
