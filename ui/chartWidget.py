# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/ShowHistoryWidget.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import Qt

import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QEvent
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPolygonF, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QGesture, QGestureEvent, QPinchGesture,QWidget

class Ui_Form(QWidget):
    def __init__(self, parent=None):
        super(Ui_Form, self).__init__(parent)
        self.setupUi(self)
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(200, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)

        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 460, 450))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.horizontalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.ch3Box = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.ch3Box.setChecked(True)
        self.ch3Box.setObjectName("ch3Box")
        self.horizontalLayout_2.addWidget(self.ch3Box)
       
        self.ch2Box = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.ch2Box.setChecked(True)
        self.ch2Box.setObjectName("ch2Box")
        self.horizontalLayout_2.addWidget(self.ch2Box)
        
        self.ch1Box = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.ch1Box.setChecked(True)
        self.ch1Box.setObjectName("ch1Box")
        self.horizontalLayout_2.addWidget(self.ch1Box)

        self.ch1Box.stateChanged.connect(self.chboxclick)
        self.ch2Box.stateChanged.connect(self.chboxclick)

        self.ch3Box.stateChanged.connect(self.chboxclick)



        
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 9)
        self.retranslateUi(Form)

        self.chart1 = chart()
        self.chart1.legend().hide()
        self.chart1.layout().setContentsMargins(0, 0, 0, 0)
        self.chart1.setBackgroundRoundness(0)
        self.view1 = QChartView(self.chart1)
        self.view1.setRenderHint(QPainter.Antialiasing)
        self.verticalLayout.addWidget(self.view1)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ch3Box.setText(_translate("Form", "ch1"))
        self.ch2Box.setText(_translate("Form", "ch2"))
        self.ch1Box.setText(_translate("Form", "ch3"))
    
    def chboxclick(self):
        widget=self.sender()
        widgetText={0:"ch1",1:"ch2",2:"ch3"}
        for i in range(3):
            if(widget.text()==widgetText[i]):
                if widget.isChecked():
                    self.add_data(self.series[i])
                else :
                    self.chart1.removeSeries(self.series[3])
                    self.chart1.removeSeries(self.series[i])
                    self.add_data(self.series[3])

    def setTitle(self,title):
        
        self.chart1.setTitle("SampleRate:  "+title+" hz ")

    def set_data(self, data):
        self.chart1.removeAllSeries()
        self.series={}
        self.color={0:Qt.red,1:Qt.blue,2:Qt.black,3:Qt.black}
        for i in range(data.shape[0]):
            print ("range:"+str(i))

            self.series[i]=self.series_to_polyline(range(len(data[i])), data[i], color=self.color[i])
            self.add_data(self.series[i])
        self.series[3]=self.series_to_polyline(range(1), [0], color=self.color[3])
        self.add_data(self.series[3])
    def add_data(self, polyline):
        self.chart1.addSeries(polyline)

        self.chart1.createDefaultAxes()
        
    def series_to_polyline(self,xdata, ydata,color=None):
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



class chart(QChart):
    def __init__(self, parent=None):
        super(QChart, self).__init__(parent)
        #self.grabGesture(Qt.PanGesture)
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
                self.scroll(-self.deltax,0)

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
                
                #self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, self.horizontalLayoutWidget.geometry().width()*p.scaleFactor() , 450))
              
                #self.zoom(p.scaleFactor())
                self.zoomX(p.scaleFactor())
                print("scaleFactor",p.scaleFactor(),"totalScaleFactor",p.totalScaleFactor())

            '''
            g=e.gesture(Qt.PanGesture) 
            if g:
               
               self.scroll(-g.delta().x(),g.delta().y())
            '''
        return True

    def zoomX( self,factor,  xcenter=1):

        rect =self.plotArea()
        widthOriginal = rect.width()
        rect.setWidth(widthOriginal / factor)
        centerScale = (xcenter / widthOriginal)

        leftOffset = (xcenter - (rect.width() * centerScale) )

        rect.moveLeft(rect.x() + leftOffset)
        self.zoomIn(rect);



    
