# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(951, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.leServerPort = QtWidgets.QLineEdit(self.centralwidget)
        self.leServerPort.setGeometry(QtCore.QRect(230, 30, 51, 26))
        self.leServerPort.setObjectName("leServerPort")
        self.btnRestartServer = QtWidgets.QPushButton(self.centralwidget)
        self.btnRestartServer.setGeometry(QtCore.QRect(290, 30, 101, 26))
        self.btnRestartServer.setObjectName("btnRestartServer")
        self.lwdClients = QtWidgets.QListWidget(self.centralwidget)
        self.lwdClients.setGeometry(QtCore.QRect(50, 70, 171, 91))
        self.lwdClients.setObjectName("lwdClients")
        self.tabClients = QtWidgets.QTabWidget(self.centralwidget)
        self.tabClients.setGeometry(QtCore.QRect(230, 70, 571, 381))
        self.tabClients.setObjectName("tabClients")
        self.btnScanDevice = QtWidgets.QPushButton(self.centralwidget)
        self.btnScanDevice.setGeometry(QtCore.QRect(130, 420, 91, 31))
        self.btnScanDevice.setObjectName("btnScanDevice")
        self.cmbServiceIp = QtWidgets.QComboBox(self.centralwidget)
        self.cmbServiceIp.setGeometry(QtCore.QRect(50, 30, 171, 26))
        self.cmbServiceIp.setObjectName("cmbServiceIp")
        self.lwdScanResult = QtWidgets.QListWidget(self.centralwidget)
        self.lwdScanResult.setGeometry(QtCore.QRect(50, 170, 171, 241))
        self.lwdScanResult.setObjectName("lwdScanResult")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 951, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabClients.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.leServerPort.setText(_translate("MainWindow", "8899"))
        self.btnRestartServer.setText(_translate("MainWindow", "restart server"))
        self.btnScanDevice.setText(_translate("MainWindow", "scan device"))

