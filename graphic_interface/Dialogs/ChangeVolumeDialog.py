# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\DuettoSystem\graphic_interface\UI_Files\ChangeVolumeDialog.ui'
#
# Created: Wed Nov 26 11:19:12 2014
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
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setTitle(_fromUtf8(""))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.rbuttonConst = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonConst.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rbuttonConst.setObjectName(_fromUtf8("rbuttonConst"))
        self.gridLayout.addWidget(self.rbuttonConst, 0, 0, 1, 1)
        self.spinboxConstValue = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.spinboxConstValue.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.spinboxConstValue.setDecimals(1)
        self.spinboxConstValue.setMinimum(0.1)
        self.spinboxConstValue.setMaximum(100.0)
        self.spinboxConstValue.setProperty("value", 1.0)
        self.spinboxConstValue.setObjectName(_fromUtf8("spinboxConstValue"))
        self.gridLayout.addWidget(self.spinboxConstValue, 0, 1, 1, 1)
        self.spinboxNormalizePercent = QtGui.QSpinBox(self.groupBox_4)
        self.spinboxNormalizePercent.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.spinboxNormalizePercent.setMinimum(1)
        self.spinboxNormalizePercent.setMaximum(10000)
        self.spinboxNormalizePercent.setProperty("value", 100)
        self.spinboxNormalizePercent.setObjectName(_fromUtf8("spinboxNormalizePercent"))
        self.gridLayout.addWidget(self.spinboxNormalizePercent, 1, 1, 1, 1)
        self.rbuttonNormalize = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonNormalize.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rbuttonNormalize.setObjectName(_fromUtf8("rbuttonNormalize"))
        self.gridLayout.addWidget(self.rbuttonNormalize, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.rbuttonFadeOut = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonFadeOut.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rbuttonFadeOut.setObjectName(_fromUtf8("rbuttonFadeOut"))
        self.gridLayout.addWidget(self.rbuttonFadeOut, 4, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.cboxModulationType = QtGui.QComboBox(self.groupBox_4)
        self.cboxModulationType.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.cboxModulationType.setEditable(False)
        self.cboxModulationType.setObjectName(_fromUtf8("cboxModulationType"))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.cboxModulationType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cboxModulationType, 2, 1, 1, 1)
        self.rbuttonFadeIn = QtGui.QRadioButton(self.groupBox_4)
        self.rbuttonFadeIn.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rbuttonFadeIn.setObjectName(_fromUtf8("rbuttonFadeIn"))
        self.gridLayout.addWidget(self.rbuttonFadeIn, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 0, 1, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Change Volume", None, QtGui.QApplication.UnicodeUTF8))
        self.rbuttonConst.setText(QtGui.QApplication.translate("Dialog", "Constant", None, QtGui.QApplication.UnicodeUTF8))
        self.rbuttonNormalize.setText(QtGui.QApplication.translate("Dialog", "Normalize", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "dB", None, QtGui.QApplication.UnicodeUTF8))
        self.rbuttonFadeOut.setText(QtGui.QApplication.translate("Dialog", "Fade Out", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.cboxModulationType.setItemText(0, QtGui.QApplication.translate("Dialog", "Linear", None, QtGui.QApplication.UnicodeUTF8))
        self.cboxModulationType.setItemText(1, QtGui.QApplication.translate("Dialog", "sin", None, QtGui.QApplication.UnicodeUTF8))
        self.cboxModulationType.setItemText(2, QtGui.QApplication.translate("Dialog", "sin-sqrt", None, QtGui.QApplication.UnicodeUTF8))
        self.cboxModulationType.setItemText(3, QtGui.QApplication.translate("Dialog", "sin^2", None, QtGui.QApplication.UnicodeUTF8))
        self.cboxModulationType.setItemText(4, QtGui.QApplication.translate("Dialog", "cuadratic", None, QtGui.QApplication.UnicodeUTF8))
        self.rbuttonFadeIn.setText(QtGui.QApplication.translate("Dialog", "Fade In", None, QtGui.QApplication.UnicodeUTF8))

