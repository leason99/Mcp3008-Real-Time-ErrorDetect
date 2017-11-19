
#!/usr/bin/python3 

import sys
import time
import numpy as np
import ctypes 
import matplotlib
matplotlib.use("Pdf")
import matplotlib.pyplot as plt
import datetime
import threading
import multiprocessing 
from multiprocessing import Process
from window import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
import pic




class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
       # self.set.clicked.connect(self.startButton)
        self.statusButton.clicked.connect(self.startButton)
        
        self.limitSlider.setMaximum(1023)
        self.limitSlider.setMinimum(0)
        self.limitSlider.setSingleStep(1)
        self.limitSlider.valueChanged.connect(self.limitSliderChange)
        self.mcp3008=Mcp3008()
        self.generateButton.clicked.connect(pic.generate)

    
    

    def startButton(self):
        if self.statusButton.text()=="start":
            self.statusButton.setText("stop")
            self.startTime=datetime.datetime.now()
            self.timer=QtCore.QTimer()
            self.timer.timeout.connect(self.update) 
            self.timer.start(1000)
            self.mcp3008.StartDetect(self.limitSlider.value())
           
        else :
            self.mcp3008.StopDetect()
            self.statusButton.setText("start")
            
            self.timer.stop()
    

    #def set(self):
        
    def limitSliderChange(self):
        value=str(self.limitSlider.value())
        self.limitValue.setText(value)

    def update(self):
        self.times=datetime.datetime.now()-self.startTime
        TotalDuration=str(self.times).split('.', 2)[0]
        print(self.times)
        self.elapsed.setText(TotalDuration)

        self.detectionTimes.setText(str(self.mcp3008.getDetectionTimes()))
        


class Mcp3008():
    
    def __init__(self):
        self.chnum=3
        self.samples=50000
        # command line: ipcrm --all=msg

        # init c lib
        self.mcp3008=ctypes.cdll.LoadLibrary("./mcp3008.so")
        self.init=self.mcp3008.init
        self.init.argtypes=(ctypes.c_int,)
        self.listener=self.mcp3008.listener
        self.stop=self.mcp3008.stop
        self.getDetectionTimes=self.mcp3008.getDetectionTimes
        self.getDetectionTimes.restype=ctypes.c_int
       
        self.detect=self.mcp3008.detect
        self.freeme=self.mcp3008.freeme
        self.getListenerData=self.mcp3008.getListenerData
        #c return type
        self.getListenerData.restype=ctypes.POINTER(ctypes.c_int32)
    
    def StartDetect(self,limit):
        self.init(limit)
        self.listener()
        #thread2=Process(target=self.detect)
        #thread2.start()
        self.detect()

    def StopDetect(self):
        self.stop()
        

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())