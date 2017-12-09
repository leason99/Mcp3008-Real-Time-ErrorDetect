#!/usr/bin/env python
from PyQt5.QtCore import QDir, Qt, QEvent
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel,
QmainWindow, QSizePolicy)
from PyQt5.QtWidgets import QGesture, QGestureEvent, QPinchGesture</strong>
class ImageViewer(QMainWindow):
def __init__(self):
super(ImageViewer, self).__init__()
self.imageLabel = QLabel()
self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
self.imageLabel.setScaledContents(True)
self.setCentralWidget(self.imageLabel)
self.setWindowTitle("Image Viewer")
self.resize(500,400)
    def event(self,e):</strong>
    if (e.type() == QEvent.Gesture):</strong>
    return self.gestureEvent(e)</strong>
    return super(QMainWindow,self).event(e)</strong>
 
    def gestureEvent(self,event):</strong>
    pinch = event.gesture(Qt.PinchGesture)</strong>
    if pinch:</strong>
    self.pinchTriggered(pinch)</strong>
    return True</strong>
 
    def pinchTriggered(self,gesture):</strong>
    self.scaleImage(gesture.scaleFactor())</strong>
def open(self):
fileName, _ = QFileDialog.getOpenFileName(self, "Open File",
QDir.currentPath())
if fileName:
image = QImage(fileName)
self.imageLabel.setPixmap(QPixmap.fromImage(image))
self.scaleFactor = 1.0
 
def scaleImage(self, factor):
self.scaleFactor *= factor
self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
 
if __name__ == '__main__':
import sys
app = QApplication(sys.argv)
imageViewer = ImageViewer()
imageViewer.show()
imageViewer.open()
imageViewer.scaleImage(imageViewer.scaleFactor)
    imageViewer.grabGesture(Qt.PinchGesture)</strong>
sys.exit(app.exec_())