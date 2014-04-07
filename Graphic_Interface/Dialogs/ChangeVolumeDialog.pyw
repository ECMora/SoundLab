# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChangeVolume.ui'
#
# Created: Tue Dec 10 14:49:23 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

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
        self.label.setObjectName(_fromUtf8("label"))
        self.rbuttonConst = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonConst.setGeometry(QtCore.QRect(10, 19, 82, 17))
        self.rbuttonConst.setObjectName(_fromUtf8("rbuttonConst"))
        self.spinboxConstValue = QtGui.QSpinBox(self.groupBox_4)
        self.spinboxConstValue.setGeometry(QtCore.QRect(100, 16, 61, 22))
        self.spinboxConstValue.setObjectName(_fromUtf8("spinboxConstValue"))
        self.cboxModulationType = QtGui.QComboBox(self.groupBox_4)
        self.cboxModulationType.setGeometry(QtCore.QRect(100, 107, 81, 22))
        self.cboxModulationType.setEditable(False)
        self.cboxModulationType.setObjectName(_fromUtf8("cboxModulationType"))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.rbuttonFadeIn = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonFadeIn.setGeometry(QtCore.QRect(10, 100, 82, 17))
        self.rbuttonFadeIn.setObjectName(_fromUtf8("rbuttonFadeIn"))
        self.rbuttonFadeOut = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonFadeOut.setGeometry(QtCore.QRect(10, 127, 82, 17))
        self.rbuttonFadeOut.setObjectName(_fromUtf8("rbuttonFadeOut"))
        self.spinboxNormalizePercent = QtGui.QSpinBox(self.groupBox_4)
        self.spinboxNormalizePercent.setGeometry(QtCore.QRect(100, 53, 61, 22))
        self.spinboxNormalizePercent.setMinimum(1)
        self.spinboxNormalizePercent.setMaximum(10000)
        self.spinboxNormalizePercent.setProperty("value", 100)
        self.spinboxNormalizePercent.setObjectName(_fromUtf8("spinboxNormalizePercent"))
        self.rbuttonNormalize = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonNormalize.setGeometry(QtCore.QRect(10, 53, 82, 17))
        self.rbuttonNormalize.setObjectName(_fromUtf8("rbuttonNormalize"))
        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(170, 55, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
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
        Dialog.setWindowTitle(_translate("Dialog", "Change Volume", None))
        self.label.setText(_translate("Dialog", "dB", None))
        self.rbuttonConst.setText(_translate("Dialog", "Constant", None))
        self.cboxModulationType.setItemText(0, _translate("Dialog", "Linear", None))
        self.cboxModulationType.setItemText(1, _translate("Dialog", "sin", None))
        self.cboxModulationType.setItemText(2, _translate("Dialog", "sin-sqrt", None))
        self.cboxModulationType.setItemText(3, _translate("Dialog", "sin^2", None))
        self.cboxModulationType.setItemText(4, _translate("Dialog", "cuadratic", None))
        self.rbuttonFadeIn.setText(_translate("Dialog", "Fade In", None))
        self.rbuttonFadeOut.setText(_translate("Dialog", "Fade Out", None))
        self.rbuttonNormalize.setText(_translate("Dialog", "Normalize", None))
        self.label_2.setText(_translate("Dialog", "%", None))


import re, sre_compile, sre_constants, sre_parse