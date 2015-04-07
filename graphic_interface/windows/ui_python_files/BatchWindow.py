# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\duetto-SoundLab\graphic_interface\UI_Files\BatchWindow.ui'
#
# Created: Mon Apr 06 14:34:53 2015
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(390, 329)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonInputFolder = QtGui.QPushButton(self.centralwidget)
        self.pushButtonInputFolder.setStyleSheet(_fromUtf8(""))
        self.pushButtonInputFolder.setFlat(False)
        self.pushButtonInputFolder.setObjectName(_fromUtf8("pushButtonInputFolder"))
        self.gridLayout.addWidget(self.pushButtonInputFolder, 0, 1, 1, 1)
        self.lineeditFilePath = QtGui.QLineEdit(self.centralwidget)
        self.lineeditFilePath.setStyleSheet(_fromUtf8(""))
        self.lineeditFilePath.setReadOnly(True)
        self.lineeditFilePath.setObjectName(_fromUtf8("lineeditFilePath"))
        self.gridLayout.addWidget(self.lineeditFilePath, 0, 0, 1, 1)
        self.lineEditOutputFolder = QtGui.QLineEdit(self.centralwidget)
        self.lineEditOutputFolder.setStyleSheet(_fromUtf8(""))
        self.lineEditOutputFolder.setReadOnly(True)
        self.lineEditOutputFolder.setObjectName(_fromUtf8("lineEditOutputFolder"))
        self.gridLayout.addWidget(self.lineEditOutputFolder, 2, 0, 1, 1)
        self.listwidgetProgress = QtGui.QListWidget(self.centralwidget)
        self.listwidgetProgress.setStyleSheet(_fromUtf8(""))
        self.listwidgetProgress.setObjectName(_fromUtf8("listwidgetProgress"))
        self.gridLayout.addWidget(self.listwidgetProgress, 3, 0, 1, 3)
        self.spboxSplitTime = QtGui.QSpinBox(self.centralwidget)
        self.spboxSplitTime.setStyleSheet(_fromUtf8(""))
        self.spboxSplitTime.setMinimum(1)
        self.spboxSplitTime.setMaximum(86400)
        self.spboxSplitTime.setProperty("value", 60)
        self.spboxSplitTime.setObjectName(_fromUtf8("spboxSplitTime"))
        self.gridLayout.addWidget(self.spboxSplitTime, 2, 2, 1, 1)
        self.pushButtonOutputFolder = QtGui.QPushButton(self.centralwidget)
        self.pushButtonOutputFolder.setStyleSheet(_fromUtf8(""))
        self.pushButtonOutputFolder.setObjectName(_fromUtf8("pushButtonOutputFolder"))
        self.gridLayout.addWidget(self.pushButtonOutputFolder, 2, 1, 1, 1)
        self.progressBarProcesed = QtGui.QProgressBar(self.centralwidget)
        self.progressBarProcesed.setProperty("value", 0)
        self.progressBarProcesed.setObjectName(_fromUtf8("progressBarProcesed"))
        self.gridLayout.addWidget(self.progressBarProcesed, 4, 0, 1, 3)
        self.pushButtonStart = QtGui.QPushButton(self.centralwidget)
        self.pushButtonStart.setObjectName(_fromUtf8("pushButtonStart"))
        self.gridLayout.addWidget(self.pushButtonStart, 5, 2, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButtonInputFolder, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.selectInputFolder)
        QtCore.QObject.connect(self.pushButtonOutputFolder, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.selectOutputFolder)
        QtCore.QObject.connect(self.pushButtonStart, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.batch)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonInputFolder.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.lineeditFilePath.setText(QtGui.QApplication.translate("MainWindow", "Select the folder of input audio files", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditOutputFolder.setText(QtGui.QApplication.translate("MainWindow", "Select the folder of output procesed files", None, QtGui.QApplication.UnicodeUTF8))
        self.spboxSplitTime.setSuffix(QtGui.QApplication.translate("MainWindow", "sec", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOutputFolder.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBarProcesed.setStyleSheet(QtGui.QApplication.translate("MainWindow", "background-color: rgb(200, 200, 255);", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStart.setText(QtGui.QApplication.translate("MainWindow", "Process", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Time Interval", None, QtGui.QApplication.UnicodeUTF8))

