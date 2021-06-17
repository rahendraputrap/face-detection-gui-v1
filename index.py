from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog,QMessageBox,QApplication
from cv2 import cv2
import numpy as np
import sys
import cv2
import face_recognition
import numpy as np
import datetime
import os

class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("index.ui", self)

        self.pushButton.clicked.connect(self.close)

        #Update time
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)

        self.image = None

        self.processedImage=None
        self.capture=cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)
        self.face_Enabled=False
        self.faceCascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def update_frame(self):
        ret,self.image=self.capture.read()
        self.image=cv2.flip(self.image,1)

        self.displayImage(self.image, 1)
        if(self.face_Enabled):
            detected_image=self.detect_face(self.image)
            self.displayImage(detected_image,2)
        else:
            self.displayImage(self.image,1)


    def detect_face(self,img):
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=self.faceCascade.detectMultiScale(gray,1.2,5,minSize=(90,90))

        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        return img

    def displayImage(self,img,window=1):
        qformat=QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888

        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        #BGR>>RGB
        outImage=outImage.rgbSwapped()

        if window==1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_OutputDialog()
    ui.show()
    sys.exit(app.exec_())