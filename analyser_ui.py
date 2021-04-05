# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'analyser.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QMainWindow(object):
    def setupUi(self, QMainWindow):
        QMainWindow.setObjectName("QMainWindow")
        QMainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QMainWindow.sizePolicy().hasHeightForWidth())
        QMainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(QMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(210, 10, 581, 581))
        self.tabWidget.setObjectName("tabWidget")
        self.tabImages = QtWidgets.QWidget()
        self.tabImages.setObjectName("tabImages")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tabImages)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 561, 531))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutImages = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutImages.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutImages.setObjectName("verticalLayoutImages")
        self.tabWidget.addTab(self.tabImages, "")
        self.tabText = QtWidgets.QWidget()
        self.tabText.setObjectName("tabText")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tabText)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 561, 531))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayoutText = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayoutText.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutText.setObjectName("verticalLayoutText")
        self.tabWidget.addTab(self.tabText, "")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 191, 581))
        self.listWidget.setObjectName("listWidget")
        QMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(QMainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(QMainWindow)

    def retranslateUi(self, QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        QMainWindow.setWindowTitle(_translate("QMainWindow", "AlphaAnalyser"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabImages), _translate("QMainWindow", "Images"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabText), _translate("QMainWindow", "Text"))
