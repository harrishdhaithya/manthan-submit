from GUI import GUI
from Detector import Detector
from tkinter import *
import cv2
import os

class Controller:
    def __init__(self,root):
        self.gui = GUI(root)
        self.cap = cv2.VideoCapture(0)
        self.detector = Detector(self.cap,"haarcascade_frontalface_default.xml")
        self.gui.detectButton.config(command=self.isPressed)
        self.detector.init_thread(self.gui.panel,self.gui.window)
        self.gui.window.wm_protocol("WM_DELETE_WINDOW",self.onClose)
        self.gui.start()
    def isPressed(self):
        if self.detector.flag ==0:
            self.detector.flag = 1
            self.gui.btn_text.set("Stop Detection")
        else:
            self.detector.flag = 0
            self.gui.btn_text.set("Start Detection")
    def onClose(self):
        self.detector.onClose()
        self.gui.onClose()
        os.abort()
        
if __name__ == "__main__":
    root = Tk()
    controller=Controller(root)
