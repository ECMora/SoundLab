# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\duetto-SoundLab\graphic_interface\UI_Files\BatchWindow.ui'
#
# Created: Tue Feb 03 14:51:47 2015
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
        MainWindow.resize(646, 362)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineeditFilePath = QtGui.QLineEdit(self.centralwidget)
        self.lineeditFilePath.setStyleSheet(_fromUtf8(""))
        self.lineeditFilePath.setObjectName(_fromUtf8("lineeditFilePath"))
        self.gridLayout.addWidget(self.lineeditFilePath, 0, 0, 1, 1)
        self.pushButtonInputFolder = QtGui.QPushButton(self.centralwidget)
        self.pushButtonInputFolder.setStyleSheet(_fromUtf8(""))
        self.pushButtonInputFolder.setFlat(False)
        self.pushButtonInputFolder.setObjectName(_fromUtf8("pushButtonInputFolder"))
        self.gridLayout.addWidget(self.pushButtonInputFolder, 0, 1, 1, 1)
        self.cbxSingleFile = QtGui.QCheckBox(self.centralwidget)
        self.cbxSingleFile.setStyleSheet(_fromUtf8(""))
        self.cbxSingleFile.setObjectName(_fromUtf8("cbxSingleFile"))
        self.gridLayout.addWidget(self.cbxSingleFile, 0, 2, 1, 1)
        self.lineEditOutputFolder = QtGui.QLineEdit(self.centralwidget)
        self.lineEditOutputFolder.setStyleSheet(_fromUtf8(""))
        self.lineEditOutputFolder.setObjectName(_fromUtf8("lineEditOutputFolder"))
        self.gridLayout.addWidget(self.lineEditOutputFolder, 1, 0, 1, 1)
        self.pushButtonOutputFolder = QtGui.QPushButton(self.centralwidget)
        self.pushButtonOutputFolder.setStyleSheet(_fromUtf8(""))
        self.pushButtonOutputFolder.setObjectName(_fromUtf8("pushButtonOutputFolder"))
        self.gridLayout.addWidget(self.pushButtonOutputFolder, 1, 1, 1, 1)
        self.listwidgetProgress = QtGui.QListWidget(self.centralwidget)
        self.listwidgetProgress.setStyleSheet(_fromUtf8(""))
        self.listwidgetProgress.setObjectName(_fromUtf8("listwidgetProgress"))
        self.gridLayout.addWidget(self.listwidgetProgress, 2, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setStyleSheet(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.rbttnDetection = QtGui.QRadioButton(self.groupBox)
        self.rbttnDetection.setStyleSheet(_fromUtf8(""))
        self.rbttnDetection.setCheckable(True)
        self.rbttnDetection.setChecked(True)
        self.rbttnDetection.setObjectName(_fromUtf8("rbttnDetection"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.rbttnDetection)
        self.rbttnSplitFile = QtGui.QRadioButton(self.groupBox)
        self.rbttnSplitFile.setStyleSheet(_fromUtf8(""))
        self.rbttnSplitFile.setObjectName(_fromUtf8("rbttnSplitFile"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.rbttnSplitFile)
        self.spboxSplitTime = QtGui.QSpinBox(self.groupBox)
        self.spboxSplitTime.setStyleSheet(_fromUtf8(""))
        self.spboxSplitTime.setMinimum(30)
        self.spboxSplitTime.setMaximum(120)
        self.spboxSplitTime.setProperty("value", 60)
        self.spboxSplitTime.setObjectName(_fromUtf8("spboxSplitTime"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spboxSplitTime)
        self.pushButtonStart = QtGui.QPushButton(self.groupBox)
        self.pushButtonStart.setObjectName(_fromUtf8("pushButtonStart"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.pushButtonStart)
        self.gridLayout.addWidget(self.groupBox, 2, 1, 1, 2)
        self.progressBarProcesed = QtGui.QProgressBar(self.centralwidget)
        self.progressBarProcesed.setProperty("value", 0)
        self.progressBarProcesed.setObjectName(_fromUtf8("progressBarProcesed"))
        self.gridLayout.addWidget(self.progressBarProcesed, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 646, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.lineeditFilePath.setText(QtGui.QApplication.translate("MainWindow", "Select the folder of input audio files", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonInputFolder.setText(QtGui.QApplication.translate("MainWindow", "Explore", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxSingleFile.setText(QtGui.QApplication.translate("MainWindow", "Single Excell", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditOutputFolder.setText(QtGui.QApplication.translate("MainWindow", "Select the folder of output procesed files", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOutputFolder.setText(QtGui.QApplication.translate("MainWindow", "Explore", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Action", None, QtGui.QApplication.UnicodeUTF8))
        self.rbttnDetection.setText(QtGui.QApplication.translate("MainWindow", "Detection", None, QtGui.QApplication.UnicodeUTF8))
        self.rbttnSplitFile.setText(QtGui.QApplication.translate("MainWindow", "Split Files", None, QtGui.QApplication.UnicodeUTF8))
        self.spboxSplitTime.setSuffix(QtGui.QApplication.translate("MainWindow", "sec", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStart.setText(QtGui.QApplication.translate("MainWindow", "Process", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBarProcesed.setStyleSheet(QtGui.QApplication.translate("MainWindow", "background-color: rgb(200, 200, 255);", None, QtGui.QApplication.UnicodeUTF8))

