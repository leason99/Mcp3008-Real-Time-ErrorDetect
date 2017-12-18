# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/ShowHistoryWidget.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(813, 626)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 801, 461))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.generateButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.generateButton.setObjectName("generateButton")
        self.verticalLayout.addWidget(self.generateButton)
        self.fileList = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.fileList.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileList.sizePolicy().hasHeightForWidth())
        self.fileList.setSizePolicy(sizePolicy)
        self.fileList.setObjectName("fileList")
        self.verticalLayout.addWidget(self.fileList)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 9)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.QchartLayout = QtWidgets.QVBoxLayout()
        self.QchartLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.QchartLayout.setObjectName("QchartLayout")
        self.horizontalLayout.addLayout(self.QchartLayout)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 10)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.generateButton.setText(_translate("Form", "Generate Image "))

