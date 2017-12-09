
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
import os
import sip
from multiprocessing import Process
#from window import Ui_MainWindow
from ui.MainWindows import Ui_MainWindow
from ui.DetectErrorWidget import Ui_Form as DetectErrorWG
from ui.ShowHistoryWidget import Ui_Form as DeteShowHistortWG

from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPolygonF, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
import pic
from PIL import Image
import webbrowser
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGesture, QGestureEvent, QPinchGesture,QWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


        #self.DetectSH=DetectShowHistort()
        self.detectErrorWG=DetectError()
        self.mainui.addWidget(self.detectErrorWG)
        self.ShowHistory.clicked.connect(self.setShowHistoryView)
        self.DetectError.clicked.connect(self.setDetectErrorView)

    def setShowHistoryView(self):
        self.mainui.removeWidget(  self.detectErrorWG)
        self.detectErrorWG.deleteLater()
        self.detectErrorWG=None

        self.DetectSH=DetectShowHistort()
        self.mainui.addWidget(self.DetectSH)

    def setDetectErrorView(self):
        self.mainui.removeWidget(self.DetectSH)
        self.DetectSH.deleteLater()
        self.DetectSH=None
        self.detectErrorWG=DetectError()
        self.mainui.addWidget(self.detectErrorWG)
        

class DetectError(QWidget,DetectErrorWG):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)

        self.statusButton.clicked.connect(self.startButton)
        self.limitSlider.setMaximum(1023)
        self.limitSlider.setMinimum(0)
        self.limitSlider.setSingleStep(1)
        self.limitSlider.valueChanged.connect(self.limitSliderChange)
        self.mcp3008=Mcp3008()
        self.generateButton.clicked.connect(self.generatePic)
        self.pushButton.clicked.connect(self.Sync)




    
   
 

    


    def generatePic(self):
        pic.generate()
        fileList=os.listdir("./pic")
        for file in fileList:
            self.fileList.addItem(file)

        
    def Sync(self):
        fileList=os.listdir("./data")
        for file in fileList:
            self.fileList.addItem(file)


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
    
    
        
    def limitSliderChange(self):
        value=str(self.limitSlider.value())
        self.limitValue.setText(value)

    def update(self):
        self.times=datetime.datetime.now()-self.startTime
        TotalDuration=str(self.times).split('.', 2)[0]
        print(self.times)
        self.elapsed.setText(TotalDuration)

        self.detectionTimes.setText(str(self.mcp3008.getDetectionTimes()))
        





class DetectShowHistort(QWidget,DeteShowHistortWG):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        self.ncurves = 0


       
        
        self.chart = QChart()
       
        self.chart.legend().hide()
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setMinimumSize(300,300)
        self.verticalLayout.addWidget(self.view)


        fileList=os.listdir("./data")
        for file in fileList:
            self.fileList.addItem(file)
        self.fileList.itemDoubleClicked.connect(self.showpic)

    def showpic(self,item):
        
        #webbrowser.open("./pic/"+item.text())
        #Image.open("./pic/"+item.text()).show()
        #os.system("open ./pic/"+item.text())

        file=open("./data/{}".format(item.text()),mode='r')
        Str=file.readline()
        strData= Str.split(",")
        data=np.array([int(n) for n in strData[:-1]],dtype=int)
        samplerate=strData[-1]
        #data struct [ch][samples]
        chnum=3
        samples=50000
        
        res=np.reshape(data,(chnum,samples)) 

        self.add_data(range(len(res[0])), res[0], color=Qt.red)
           
    
    def add_data(self, xdata, ydata, color=None):
        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(.1)
        curve.setPen(pen)
        curve.setUseOpenGL(True)
        curve.append(self.series_to_polyline(xdata, ydata))
        
        self.chart.removeAllSeries()

        self.chart.addSeries(curve)
        self.chart.createDefaultAxes()
        self.ncurves += 1

    def series_to_polyline(self,xdata, ydata):
        """Convert series data to QPolygon(F) polyline

        This code is derived from PythonQwt's function named 
        `qwt.plot_curve.series_to_polyline`"""
        size = len(xdata)
        polyline = QPolygonF(size)
        pointer = polyline.data()
        dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
        pointer.setsize(2*polyline.size()*tinfo(dtype).dtype.itemsize)
        memory = np.frombuffer(pointer, dtype)
        memory[:(size-1)*2+1:2] = xdata
        memory[1:(size-1)*2+2:2] = ydata
        return polyline    






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