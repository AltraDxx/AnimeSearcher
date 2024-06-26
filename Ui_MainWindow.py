# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MyProj\AnimeSearcher\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1150, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_12.addWidget(self.label_25)
        self.txtFile = QtWidgets.QLineEdit(self.centralwidget)
        self.txtFile.setReadOnly(True)
        self.txtFile.setObjectName("txtFile")
        self.horizontalLayout_12.addWidget(self.txtFile)
        self.btnFile = QtWidgets.QPushButton(self.centralwidget)
        self.btnFile.setMinimumSize(QtCore.QSize(50, 0))
        self.btnFile.setMaximumSize(QtCore.QSize(50, 16777215))
        self.btnFile.setObjectName("btnFile")
        self.horizontalLayout_12.addWidget(self.btnFile)
        self.horizontalLayout_12.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(770, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(770, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tbResult = QtWidgets.QTableWidget(self.groupBox_2)
        self.tbResult.setMinimumSize(QtCore.QSize(0, 0))
        self.tbResult.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbResult.setAlternatingRowColors(True)
        self.tbResult.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tbResult.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbResult.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tbResult.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tbResult.setObjectName("tbResult")
        self.tbResult.setColumnCount(3)
        self.tbResult.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbResult.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbResult.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbResult.setHorizontalHeaderItem(2, item)
        self.verticalLayout_3.addWidget(self.tbResult)
        self.horizontalLayout_13.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 125))
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 999999))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.widget = QVideoWidget(self.groupBox)
        self.widget.setMinimumSize(QtCore.QSize(320, 180))
        self.widget.setMaximumSize(QtCore.QSize(320, 180))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2.addWidget(self.widget)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.verticalLayout.setStretch(0, 1)
        self.horizontalLayout_13.addWidget(self.groupBox)
        self.horizontalLayout_13.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_13)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1150, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.btnFile.clicked.connect(MainWindow.btnFile_clicked) # type: ignore
        self.tbResult.itemSelectionChanged.connect(MainWindow.tbResult_itemSelectionChanged) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "以图搜番 @Dxx"))
        self.label_25.setText(_translate("MainWindow", "图片"))
        self.btnFile.setText(_translate("MainWindow", "选择"))
        self.groupBox_2.setTitle(_translate("MainWindow", "结果"))
        item = self.tbResult.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "图片"))
        item = self.tbResult.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "标题"))
        item = self.tbResult.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "相似度"))
        self.groupBox.setTitle(_translate("MainWindow", "详情"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">{}</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">{}</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#5500ff;\">别名：</span><span style=\" font-size:11pt;\">    {}</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#5500ff;\">文件：</span><span style=\" font-size:11pt;\">    {}</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#5500ff;\">章节：</span><span style=\" font-size:11pt;\">    {}</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#5500ff;\">时间：</span><span style=\" font-size:11pt;\">    {}</span></p></body></html>"))
from PyQt5.QtMultimediaWidgets import QVideoWidget
