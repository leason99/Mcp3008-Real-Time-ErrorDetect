# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/DetectErrorWidget.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(433, 489)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 381, 462))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ch1layout = QtWidgets.QHBoxLayout()
        self.ch1layout.setObjectName("ch1layout")
        self.ch1box = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ch1box.setChecked(True)
        self.ch1box.setObjectName("ch1box")
        self.ch1layout.addWidget(self.ch1box)
        self.ch1limit = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ch1limit.setObjectName("ch1limit")
        self.ch1layout.addWidget(self.ch1limit)
        self.ch1limitValue = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ch1limitValue.setEnabled(True)
        self.ch1limitValue.setText("")
        self.ch1limitValue.setObjectName("ch1limitValue")
        self.ch1layout.addWidget(self.ch1limitValue)
        self.ch1limitSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.ch1limitSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ch1limitSlider.setObjectName("ch1limitSlider")
        self.ch1layout.addWidget(self.ch1limitSlider)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.ch1layout.addWidget(self.pushButton)
        self.verticalLayout_4.addLayout(self.ch1layout)
        self.ch2layout = QtWidgets.QHBoxLayout()
        self.ch2layout.setObjectName("ch2layout")
        self.ch2box = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ch2box.setChecked(True)
        self.ch2box.setObjectName("ch2box")
        self.ch2layout.addWidget(self.ch2box)
        self.ch2limit = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ch2limit.setObjectName("ch2limit")
        self.ch2layout.addWidget(self.ch2limit)
        self.ch2limitValue = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ch2limitValue.setEnabled(True)
        self.ch2limitValue.setText("")
        self.ch2limitValue.setObjectName("ch2limitValue")
        self.ch2layout.addWidget(self.ch2limitValue)
        self.ch2limitSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.ch2limitSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ch2limitSlider.setObjectName("ch2limitSlider")
        self.ch2layout.addWidget(self.ch2limitSlider)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.ch2layout.addWidget(self.pushButton_2)
        self.verticalLayout_4.addLayout(self.ch2layout)
        self.ch3layout = QtWidgets.QHBoxLayout()
        self.ch3layout.setObjectName("ch3layout")
        self.ch3checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ch3checkBox.setChecked(True)
        self.ch3checkBox.setObjectName("ch3checkBox")
        self.ch3layout.addWidget(self.ch3checkBox)
        self.ch3limit = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ch3limit.setObjectName("ch3limit")
        self.ch3layout.addWidget(self.ch3limit)
        self.ch3limitValue = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ch3limitValue.setEnabled(True)
        self.ch3limitValue.setText("")
        self.ch3limitValue.setObjectName("ch3limitValue")
        self.ch3layout.addWidget(self.ch3limitValue)
        self.ch3limitSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.ch3limitSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ch3limitSlider.setObjectName("ch3limitSlider")
        self.ch3layout.addWidget(self.ch3limitSlider)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.ch3layout.addWidget(self.pushButton_3)
        self.verticalLayout_4.addLayout(self.ch3layout)
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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ch1box.setText(_translate("Form", "ch1"))
        self.ch1limit.setText(_translate("Form", "limit"))
        self.pushButton.setText(_translate("Form", "set"))
        self.ch2box.setText(_translate("Form", "ch2"))
        self.ch2limit.setText(_translate("Form", "limit"))
        self.pushButton_2.setText(_translate("Form", "set"))
        self.ch3checkBox.setText(_translate("Form", "ch3"))
        self.ch3limit.setText(_translate("Form", "limit"))
        self.pushButton_3.setText(_translate("Form", "set"))
        self.statusButton.setText(_translate("Form", "start"))
        self.label.setText(_translate("Form", "Time:"))
        self.elapsed.setText(_translate("Form", "0:00:00"))
        self.label_5.setText(_translate("Form", "Detected"))
        self.detectionTimes.setText(_translate("Form", "0"))

