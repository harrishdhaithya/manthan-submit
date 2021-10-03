from tkinter import *
from tkinter import StringVar

class GUI:
    def __init__(self,root):
        self.window = root
        self.panel = None

        self.btn_text=StringVar()
        self.detectButton = Button(self.window,textvariable=self.btn_text)
        self.btn_text.set("Start Detection")
        self.detectButton.pack(side="bottom",fill="x",expand="yes",padx=10,pady=0)

        self.window.wm_title("face Detection")
        self.window.wm_protocol("WM_DELETE_WINDOW",self.onClose)
    def start(self):
        self.window.mainloop()
    def onClose(self):
        print("Closing...")
        self.window.quit()
        self.window.destroy()
