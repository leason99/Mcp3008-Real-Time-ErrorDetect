# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(620, 528)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        #self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 500, 500))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.verticalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout_4")

        
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        #self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.limit = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.limit.setObjectName("limit")
        self.horizontalLayout_7.addWidget(self.limit)
        self.limitValue = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.limitValue.setEnabled(True)
        self.limitValue.setText("")
        self.limitValue.setObjectName("limitValue")
        self.horizontalLayout_7.addWidget(self.limitValue)
        self.limitSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.limitSlider.setOrientation(QtCore.Qt.Horizontal)
        self.limitSlider.setObjectName("limitSlider")
        self.horizontalLayout_7.addWidget(self.limitSlider)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_7.addWidget(self.pushButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.statusButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.statusButton.setObjectName("statusButton")
        self.horizontalLayout_8.addWidget(self.statusButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.elapsed = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.elapsed.setObjectName("elapsed")
        self.horizontalLayout_3.addWidget(self.elapsed)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.detectionTimes = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.detectionTimes.setObjectName("detectionTimes")
        self.horizontalLayout_2.addWidget(self.detectionTimes)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.generateButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.generateButton.setObjectName("generateButton")
        self.verticalLayout_4.addWidget(self.generateButton)
        self.fileList = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.fileList.setObjectName("fileList")
        self.verticalLayout_4.addWidget(self.fileList)

        self.horizontalLayout.addLayout(self.verticalLayout_4)




        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 620, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.limit.setText(_translate("MainWindow", "limit"))
        self.pushButton.setText(_translate("MainWindow", "set"))
        self.statusButton.setText(_translate("MainWindow", "start"))
        self.label.setText(_translate("MainWindow", "Time:"))
        self.elapsed.setText(_translate("MainWindow", "0:00:00"))
        self.label_5.setText(_translate("MainWindow", "Detected"))
        self.detectionTimes.setText(_translate("MainWindow", "0"))
        self.generateButton.setText(_translate("MainWindow", "Generate Image "))

