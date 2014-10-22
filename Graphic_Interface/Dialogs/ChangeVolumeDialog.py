# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Biologia\SISTEMA\DuettoSystem\graphic_interface\UI Files\ChangeVolume.ui'
#
# Created: Fri Apr 25 12:05:19 2014
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(318, 212)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(220, 10, 81, 71))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 10, 201, 181))
        self.groupBox_4.setTitle(_fromUtf8(""))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.label = QtGui.QLabel(self.groupBox_4)
        self.label.setGeometry(QtCore.QRect(170, 20, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.rbuttonConst = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonConst.setGeometry(QtCore.QRect(10, 19, 82, 17))
        self.rbuttonConst.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rbuttonConst.setObjectName(_fromUtf8("rbuttonConst"))
        self.spinboxConstValue = QtGui.QSpinBox(self.groupBox_4)
        self.spinboxConstValue.setGeometry(QtCore.QRect(100, 16, 61, 22))
        self.spinboxConstValue.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.spinboxConstValue.setMinimum(-200)
        self.spinboxConstValue.setObjectName(_fromUtf8("spinboxConstValue"))
        self.cboxModulationType = QtGui.QComboBox(self.groupBox_4)
        self.cboxModulationType.setGeometry(QtCore.QRect(100, 107, 81, 22))
        self.cboxModulationType.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.cboxModulationType.setEditable(False)
        self.cboxModulationType.setObjectName(_fromUtf8("cboxModulationType"))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.rbuttonFadeIn = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonFadeIn.setGeometry(QtCore.QRect(10, 100, 82, 17))
        self.rbuttonFadeIn.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rbuttonFadeIn.setObjectName(_fromUtf8("rbuttonFadeIn"))
        self.rbuttonFadeOut = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonFadeOut.setGeometry(QtCore.QRect(10, 127, 82, 17))
        self.rbuttonFadeOut.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rbuttonFadeOut.setObjectName(_fromUtf8("rbuttonFadeOut"))
        self.spinboxNormalizePercent = QtGui.QSpinBox(self.groupBox_4)
        self.spinboxNormalizePercent.setGeometry(QtCore.QRect(100, 53, 61, 22))
        self.spinboxNormalizePercent.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.spinboxNormalizePercent.setMinimum(1)
        self.spinboxNormalizePercent.setMaximum(10000)
        self.spinboxNormalizePercent.setProperty("value", 100)
        self.spinboxNormalizePercent.setObjectName(_fromUtf8("spinboxNormalizePercent"))
        self.rbuttonNormalize = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonNormalize.setGeometry(QtCore.QRect(10, 53, 82, 17))
        self.rbuttonNormalize.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rbuttonNormalize.setObjectName(_fromUtf8("rbuttonNormalize"))
        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(170, 55, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(220, 380, 251, 51))
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Change Volume", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "dB", None, QtGui.QApplication.UnicodeUTF8))
        self.rbuttonConst.setText(QtGui.QApplication.translate("Dialog", "Constant", None, QtGui.QApplication.UnicodeUTF8))
        self.cboxModulationType.setItemText(0, QtGui.QApplication.translate("Dialog", "Linear", None, QtGui.QApplication.UnicodeUTF8))
        self.cboxModulationType.setItemText(1, QtGui.QApplication.translate("Dialog", "sin", None, QtGui.QApplication.UnicodeUTF8))
        self.cboxModulationType.setItemText(2, QtGui.QApplication.translate("Dialog", "sin-sqrt", None, QtGui.QApplication.UnicodeUTF8))
        self.cboxModulationType.setItemText(3, QtGui.QApplication.translate("Dialog", "sin^2", None, QtGui.QApplication.UnicodeUTF8))
        self.cboxModulationType.setItemText(4, QtGui.QApplication.translate("Dialog", "cuadratic", None, QtGui.QApplication.UnicodeUTF8))
        self.rbuttonFadeIn.setText(QtGui.QApplication.translate("Dialog", "Fade In", None, QtGui.QApplication.UnicodeUTF8))
        self.rbuttonFadeOut.setText(QtGui.QApplication.translate("Dialog", "Fade Out", None, QtGui.QApplication.UnicodeUTF8))
        self.rbuttonNormalize.setText(QtGui.QApplication.translate("Dialog", "Normalize", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "%", None, QtGui.QApplication.UnicodeUTF8))

