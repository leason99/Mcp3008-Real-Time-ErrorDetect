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
import webbrowser
import pic

import shutil

from PyQt5.QtCore import Qt


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QEvent,QSize
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPolygonF, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QGesture, QGestureEvent, QPinchGesture,QWidget


from PIL import Image


from multiprocessing import Process
#from window import Ui_MainWindow
from ui.MainWindows import Ui_MainWindow
from ui.DetectErrorWidget import Ui_Form as DetectErrorWG
from ui.ShowHistoryWidget import Ui_Form as DeteShowHistortWG
from ui.singleTrigerWidget import Ui_Form as singleTrigerWG
from ui.chartWidget import Ui_Form as chartWG

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.grabGesture(Qt.PanGesture)
        self.grabGesture(Qt.PinchGesture)

        self.DetectSH=None
        self.SingleTriger=None
        self.detectErrorWG=DetectError()
        self.DetectError.setEnabled(False)
        self.mainui.addWidget(self.detectErrorWG)
        self.ShowHistory.clicked.connect(self.setShowHistoryView)
        self.DetectError.clicked.connect(self.setDetectErrorView)
        self.DetectInstant.clicked.connect(self.setSingleTriger)
        self.quit.clicked.connect(self.Quit)
    '''
    def event(self,event) :
        print("event",event.type())

        if event.type() == QEvent.Gesture  :
            print("gestureEvent") 
        return False
    '''
    def Quit(self):
        sys.exit()
    def setShowHistoryView(self):
        if self.detectErrorWG:
            self.mainui.removeWidget(  self.detectErrorWG)
            self.detectErrorWG.deleteLater()
            self.detectErrorWG=None
            self.DetectError.setEnabled(True)

        if self.DetectSH:
            self.mainui.removeWidget(self.DetectSH)
            self.DetectSH.deleteLater()
            self.DetectSH=None
            self.ShowHistory.setEnabled(True)

        if  self.SingleTriger:
            self.mainui.removeWidget(self.SingleTriger)
            self.SingleTriger.deleteLater()
            self.SingleTriger=None
            self.DetectInstant.setEnabled(True)

        self.sender().setEnabled(False)

        self.DetectSH=DetectShowHistort()
        self.mainui.addWidget(self.DetectSH)

    def setDetectErrorView(self):
        if self.detectErrorWG:
            self.mainui.removeWidget(  self.detectErrorWG)
            self.detectErrorWG.deleteLater()
            self.detectErrorWG=None
            self.DetectError.setEnabled(True)
            
        if self.DetectSH:
            self.mainui.removeWidget(self.DetectSH)
            self.DetectSH.deleteLater()
            self.DetectSH=None
            self.ShowHistory.setEnabled(True)

        if  self.SingleTriger:
            self.mainui.removeWidget(self.SingleTriger)
            self.SingleTriger.deleteLater()
            self.SingleTriger=None
            self.DetectInstant.setEnabled(True)

        self.sender().setEnabled(False)


        self.detectErrorWG=DetectError()
        self.mainui.addWidget(self.detectErrorWG)

    def setSingleTriger(self) :
        
        if self.detectErrorWG:
            self.mainui.removeWidget(  self.detectErrorWG)
            self.detectErrorWG.deleteLater()
            self.detectErrorWG=None
            self.DetectError.setEnabled(True)
            
        if self.DetectSH:
            self.mainui.removeWidget(self.DetectSH)
            self.DetectSH.deleteLater()
            self.DetectSH=None
            self.ShowHistory.setEnabled(True)

        if  self.SingleTriger:
            self.mainui.removeWidget(self.SingleTriger)
            self.SingleTriger.deleteLater()
            self.SingleTriger=None
            self.DetectInstant.setEnabled(True)

        self.sender().setEnabled(False)

        self.SingleTriger=singleTriger()
        self.mainui.addWidget(self.SingleTriger)

        

class singleTriger(QWidget,singleTrigerWG):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)

        self.statusButton.clicked.connect(self.startButton)
        self.ch1limitSlider.setMaximum(1023)
        self.ch1limitSlider.setMinimum(0)
        self.ch1limitSlider.setSingleStep(1)
        self.ch1limitSlider.valueChanged.connect(self.limitSliderChange)

        self.ch2limitSlider.setMaximum(1023)
        self.ch2limitSlider.setMinimum(0)
        self.ch2limitSlider.setSingleStep(1)
        self.ch2limitSlider.valueChanged.connect(self.limitSliderChange)

        self.ch3limitSlider.setMaximum(1023)
        self.ch3limitSlider.setMinimum(0)
        self.ch3limitSlider.setSingleStep(1)
        self.ch3limitSlider.valueChanged.connect(self.limitSliderChange)
        '''
        self.trigerChart=chart()
        self.trigerChart.layout().setContentsMargins(0, 0, 0, 0)
        self.trigerChart.setBackgroundRoundness(0)
        self.trigerView = QChartView(self.trigerChart)
        self.trigerView.setRenderHint(QPainter.Antialiasing)
        '''
        

        self.trigerChart=chartWG()
        self.trigerChart.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 600, 300))
        self.verticalLayout_4.addWidget(self.trigerChart)
        self.mcp3008=Mcp3008()

    def startButton(self):
        if self.statusButton.text()=="start":
            self.statusButton.setText("stop")
            self.startTime=datetime.datetime.now()
            self.timer=QtCore.QTimer()
            self.timer.timeout.connect(self.update) 
            self.timer.start(1000)
            
            if self.ch1box.isChecked() :
                ch1Value=self.ch1limitSlider.value()
            else :
                ch1Value=2000


            if self.ch2box.isChecked() :
                ch2Value=self.ch2limitSlider.value()
            else :
                ch2Value=2000
            
            if self.ch3checkBox.isChecked() :
                ch3Value=self.ch3limitSlider.value()
            else :
                ch3Value=2000
            
            self.mcp3008.StartDetectOnce(ch1Value,ch2Value,ch3Value)

        else :
            
            self.mcp3008.StopDetect()
            self.statusButton.setText("start")
            
            self.timer.stop()
    
    
        
    def limitSliderChange(self):
        
        Slider = self.sender()
        value=str(Slider.value())
        if Slider == self.ch1limitSlider:
            self.ch1limitValue.setText(value)

        elif  Slider == self.ch2limitSlider:
            self.ch2limitValue.setText(value)

        elif  Slider == self.ch3limitSlider:
            self.ch3limitValue.setText(value)


    def update(self):
        self.times=datetime.datetime.now()-self.startTime
        TotalDuration=str(self.times).split('.', 2)[0]
        print(self.times)
        self.elapsed.setText(TotalDuration)
        self.detectionTimes.setText(str(self.mcp3008.getDetectionTimes()))
        if self.mcp3008.recValueOnceIsEnd() :
            print("self.mcp3008.StopDetect()")

            self.mcp3008.StopDetect()

            buf =self.mcp3008.getSingleTrigerBuf()



           # ArrayType = ctypes.c_int*3*50000
            #array_pointer = ctypes.cast(buf, ctypes.POINTER(ArrayType))
            #a = np.frombuffer(array_pointer.contents)
            a = np.fromiter(buf, dtype=np.int, count=3*50000) # copy

            print(a)
            
            self.res=a.reshape(3,int (a .shape[0]/3))
            self.trigerChart.set_data(self.res)
            '''
            self.line0=self.trigerChart.series_to_polyline(range(1), [0], color=Qt.black)
            self.line1=self.trigerChart.series_to_polyline(range(len(self.res[0])), self.res[0], color=Qt.red)
            self.line2=self.trigerChart.series_to_polyline(range(len(self.res[1])), self.res[1], color=Qt.blue)
            self.line3=self.trigerChart.series_to_polyline(range(len(self.res[2])), self.res[2], color=Qt.black)           
            
            
            self.trigerChart.add_data(self.line0)
            self.trigerChart.add_data(self.line1)
            self.trigerChart.add_data(self.line2)
            self.trigerChart.add_data(self.line3)

            '''
            
            self.statusButton.setText("start")
            self.timer.stop()

class DetectError(QWidget,DetectErrorWG):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)

        self.statusButton.clicked.connect(self.startButton)
        self.ch1limitSlider.setMaximum(1023)
        self.ch1limitSlider.setMinimum(0)
        self.ch1limitSlider.setSingleStep(1)
        self.ch1limitSlider.valueChanged.connect(self.limitSliderChange)

        self.ch2limitSlider.setMaximum(1023)
        self.ch2limitSlider.setMinimum(0)
        self.ch2limitSlider.setSingleStep(1)
        self.ch2limitSlider.valueChanged.connect(self.limitSliderChange)

        self.ch3limitSlider.setMaximum(1023)
        self.ch3limitSlider.setMinimum(0)
        self.ch3limitSlider.setSingleStep(1)
        self.ch3limitSlider.valueChanged.connect(self.limitSliderChange)


        self.mcp3008=Mcp3008()
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
            
            if self.ch1box.isChecked() :
                ch1Value=self.ch1limitSlider.value()
            else :
                ch1Value=2000


            if self.ch2box.isChecked() :
                ch2Value=self.ch2limitSlider.value()
            else :
                ch2Value=2000
            
            if self.ch3checkBox.isChecked() :
                ch3Value=self.ch3limitSlider.value()
            else :
                ch3Value=2000
            
            self.mcp3008.StartDetect(ch1Value,ch2Value,ch3Value)

        else :
            
            self.mcp3008.StopDetect()
            self.statusButton.setText("start")
            self.timer.stop()
    
    
        
    def limitSliderChange(self):
        
        Slider = self.sender()
        value=str(Slider.value())
        if Slider == self.ch1limitSlider:
            self.ch1limitValue.setText(value)

        elif  Slider == self.ch2limitSlider:
            self.ch2limitValue.setText(value)

        elif  Slider == self.ch3limitSlider:
            self.ch3limitValue.setText(value)


    def update(self):
        self.times=datetime.datetime.now()-self.startTime
        TotalDuration=str(self.times).split('.', 2)[0]
        print(self.times)
        self.elapsed.setText(TotalDuration)

        self.detectionTimes.setText(str(self.mcp3008.getDetectionTimes()))
        
class chart(QChart):
    def __init__(self, parent=None):
        super(QChart, self).__init__(parent)
        self.grabGesture(Qt.PanGesture)
        self.grabGesture(Qt.PinchGesture)
        self.x=0
        self.y=0
        self.deltax=0
        self.deltay=0
        #self.installSceneEventFilter(self.sceneEvent)
    def sceneEvent(self,event) :
    #def event(self,event) :
        print("sceneEvent",event.type())
        
        if event.type() == QEvent.Gesture  :
            print("gestureEvent")
            return self.gestureEvent(QGestureEvent(event))
        
        if (event.type() ==QEvent.GraphicsSceneMousePress | event.type() ==QEvent.GraphicsSceneMouseRelease):
            #m=QGraphicsSceneMouseEvent()
            
            self.x=event.buttonDownPos(Qt.LeftButton).x()
            self.y=event.buttonDownPos(Qt.LeftButton).y()
            self.deltax=0
            self.deltay=0
        

        elif event.type() ==QEvent.GraphicsSceneMouseMove:
        
            

            self.deltax=event.lastPos().x()-self.x
            self.deltay=event.lastPos().y()-self.y
            
            if not (self.x==0 and  self.y==0):
                self.scroll(-self.deltax,self.deltay)

            self.x=event.lastPos().x()
            self.y=event.lastPos().y()
        elif event.GraphicsSceneMouseRelease:
            self.x=0
            self.y=0
            pass
        

        return True
        
    def gestureEvent(self, e):
        if e.type()==QEvent.Gesture:
            p=e.gesture(Qt.PinchGesture)
            if p:
            
                self.zoom(p.scaleFactor())
                print("scaleFactor",p.scaleFactor(),"totalScaleFactor",p.totalScaleFactor())
            
            
            g=e.gesture(Qt.PanGesture) 
            if g:
               
               self.scroll(-g.delta().x(),g.delta().y())
            
    
          
      
            ''' if not g.state()==Qt.GestureFinished: continue
                if g.gestureType()==self._upLeftType:
                    self.setAll()
                    e.setAccepted(g, True)
                    return True
                elif g.gestureType()==self._cancelType:
                    self.clearAll()
                    e.setAccepted(g, True)
                    return True b x
                else: continue
            '''
        return True

    def add_data(self, polyline):
        
        
        self.addSeries(polyline)
        self.createDefaultAxes()
        
    def series_to_polyline(self,xdata, ydata,color=None):
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

        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(.1)
        curve.setPen(pen)
        curve.setUseOpenGL(True)
        curve.append(polyline)

        return curve    






class DetectShowHistort(QWidget,DeteShowHistortWG):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)

        self.grabGesture(Qt.PanGesture)
        self.grabGesture(Qt.PinchGesture)
        self.generateButton.clicked.connect(self.generatePic)
        self.chart1 = chartWG()
        '''
        self.chart1 = chart()
        self.chart1.legend().hide()

        self.chart1.layout().setContentsMargins(0, 0, 0, 0)
        self.chart1.setBackgroundRoundness(0)
        self.view1 = QChartView(self.chart1)
        self.view1.setRenderHint(QPainter.Antialiasing)
        '''
     
        self.QchartLayout.addWidget(self.chart1)
        '''
        self.ch1Box.stateChanged.connect(self.chboxclick)
        self.ch2Box.stateChanged.connect(self.chboxclick)

        self.ch3Box.stateChanged.connect(self.chboxclick)
        '''

        if not os.path.exists("./data"):
            os.mkdir("./data",mode=0o777)
            shutil.chown("./data", user="pi", group="pi")
        fileList=os.listdir("./data")
        fileList.sort()
        for file in fileList:
            self.fileList.addItem(file)

        for i in range (self.fileList.count()):
            self.fileList.item(i).setSizeHint(QSize(self.fileList.item(i).sizeHint().width(),30))
            
        self.fileList.itemDoubleClicked.connect(self.showpic)
    def generatePic(self):
        pic.generate()

    def showpic(self,item):
        waitCursor=QCursor()
        waitCursor.setShape(Qt.WaitCursor);
        self.setCursor(waitCursor);


   
    
        #webbrowser.open("./pic/"+item.text())
        #Image.open("./pic/"+item.text()).show()
        #os.system("open ./pic/"+item.text())

        file=open("./data/{}".format(item.text()),mode='r')

        #data struct [ch][samples]

        Str=file.read()

        strData= Str.split("\n")
       
        chnum=len(strData)-1
        samplerate=strData[-1]
        data=np.array([int(n) for x in strData[:-1] for n in x.split(",")[:-1]  ],dtype=int)
        print(data.shape)
        print(int (data.shape[0]/chnum))
        self.res=data.reshape(chnum,int (data.shape[0]/chnum))
        
        self.chart1.set_data(self.res)
        self.chart1.setTitle(samplerate)


        waitCursor.setShape(Qt.ArrowCursor);
        self.setCursor(waitCursor);


        '''
        self.line0=self.series_to_polyline(range(1), [0], color=Qt.black)
        self.line1=self.series_to_polyline(range(len(self.res[0])), self.res[0], color=Qt.red)
        self.line2=self.series_to_polyline(range(len(self.res[1])), self.res[1], color=Qt.blue)
        self.line3=self.series_to_polyline(range(len(self.res[2])), self.res[2], color=Qt.black)
     
        self.chart1.removeAllSeries()

        if self.ch1Box.isChecked():
            self.add_data(self.chart1,self.line1)

        if self.ch2Box.isChecked():
            self.add_data(self.chart1,self.line2)

        if self.ch3Box.isChecked():
            self.add_data(self.chart1,self.line3)
        '''
    def chboxclick(self):
        widget=self.sender()
        
        if(widget.text()=="ch1"):
            line=self.line1
            color=Qt.red
        elif(widget.text()=="ch2"):
            line=self.line2
            color=Qt.blue
        elif(widget.text()=="ch3"):
            line=self.line3
            color=Qt.black

        if widget.isChecked():
            self.add_data(self.chart1,line)
        else :
            self.chart1.removeSeries(line)
            self.chart1.removeSeries(self.line0)
            self.add_data(self.chart1,self.line0)




    def add_data(self,chart, polyline):
        
        
        chart.addSeries(polyline)
        chart.createDefaultAxes()
        
    def series_to_polyline(self,xdata, ydata,color=None):
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

        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(.1)
        curve.setPen(pen)
        curve.setUseOpenGL(True)
        curve.append(polyline)

        return curve    






class Mcp3008():
    
    def __init__(self):
        self.chnum=3
        self.samples=50000
        # command line: ipcrm --all=msg

        # init c lib
        self.mcp3008=ctypes.cdll.LoadLibrary("./mcp3008.so")
        self.init=self.mcp3008.init
        self.init.argtypes=(ctypes.c_int,ctypes.c_int,ctypes.c_int)
        self.listener=self.mcp3008.listener
        self.stop=self.mcp3008.stop
        self.getDetectionTimes=self.mcp3008.getDetectionTimes
        self.getDetectionTimes.restype=ctypes.c_int
        self.listenerOnce=self.mcp3008.listenerOnce
        self.recValueOnceIsEnd=self.mcp3008.recValueOnceIsEnd
        self.recValueOnceIsEnd.restype=ctypes.c_int#

        self.getSingleTrigerBuf=self.mcp3008.getSingleTrigerBuf
        self.getSingleTrigerBuf.restype=ctypes.POINTER(ctypes.c_int)#


        self.detect=self.mcp3008.detect
        self.freeme=self.mcp3008.freeme
        self.getListenerData=self.mcp3008.getListenerData
        #c return type
        self.getListenerData.restype=ctypes.POINTER(ctypes.c_int)#
    
    def StartDetect(self,ch1Value,ch2Value,ch3Value):
        self.init(ch1Value,ch2Value,ch3Value)
        self.listener()
        #thread2=Process(target=self.detect)
        #thread2.start()
        self.detect()

    def StartDetectOnce(self,ch1Value,ch2Value,ch3Value):
        self.init(ch1Value,ch2Value,ch3Value)
        self.listenerOnce()
        #thread2=Process(target=self.detect)
        #thread2.start()
        self.detect()

    def StopDetect(self):
        self.stop()
        

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()








    window.showFullScreen()
    #window.show()
    sys.exit(app.exec_())