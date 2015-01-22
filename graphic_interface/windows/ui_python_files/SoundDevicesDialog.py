# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\duetto-SoundLab\graphic_interface\UI_Files\SoundDevicesDialog.ui'
#
# Created: Thu Jan 22 11:34:35 2015
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
        Dialog.resize(214, 307)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btonaceptar = QtGui.QPushButton(Dialog)
        self.btonaceptar.setToolTip(_fromUtf8(""))
        self.btonaceptar.setCheckable(False)
        self.btonaceptar.setDefault(False)
        self.btonaceptar.setFlat(False)
        self.btonaceptar.setObjectName(_fromUtf8("btonaceptar"))
        self.gridLayout.addWidget(self.btonaceptar, 2, 0, 1, 1)
        self.btoncancelar = QtGui.QPushButton(Dialog)
        self.btoncancelar.setToolTip(_fromUtf8(""))
        self.btoncancelar.setDefault(False)
        self.btoncancelar.setObjectName(_fromUtf8("btoncancelar"))
        self.gridLayout.addWidget(self.btoncancelar, 2, 1, 1, 1)
        self.grpBoxInput = QtGui.QGroupBox(Dialog)
        self.grpBoxInput.setObjectName(_fromUtf8("grpBoxInput"))
        self.verticalLayout = QtGui.QVBoxLayout(self.grpBoxInput)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.inputDevice_cbox = QtGui.QComboBox(self.grpBoxInput)
        self.inputDevice_cbox.setObjectName(_fromUtf8("inputDevice_cbox"))
        self.verticalLayout.addWidget(self.inputDevice_cbox)
        self.inputDevice_lbl = QtGui.QLabel(self.grpBoxInput)
        self.inputDevice_lbl.setObjectName(_fromUtf8("inputDevice_lbl"))
        self.verticalLayout.addWidget(self.inputDevice_lbl)
        self.gridLayout.addWidget(self.grpBoxInput, 0, 0, 1, 2)
        self.grpBoxOutput = QtGui.QGroupBox(Dialog)
        self.grpBoxOutput.setObjectName(_fromUtf8("grpBoxOutput"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.grpBoxOutput)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.outputDevice_cbox = QtGui.QComboBox(self.grpBoxOutput)
        self.outputDevice_cbox.setObjectName(_fromUtf8("outputDevice_cbox"))
        self.verticalLayout_2.addWidget(self.outputDevice_cbox)
        self.outputDevice_lbl = QtGui.QLabel(self.grpBoxOutput)
        self.outputDevice_lbl.setObjectName(_fromUtf8("outputDevice_lbl"))
        self.verticalLayout_2.addWidget(self.outputDevice_lbl)
        self.gridLayout.addWidget(self.grpBoxOutput, 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.btonaceptar, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QObject.connect(self.btoncancelar, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Sound Devices", None, QtGui.QApplication.UnicodeUTF8))
        self.btonaceptar.setText(QtGui.QApplication.translate("Dialog", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.btoncancelar.setText(QtGui.QApplication.translate("Dialog", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.grpBoxInput.setTitle(QtGui.QApplication.translate("Dialog", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.inputDevice_lbl.setText(QtGui.QApplication.translate("Dialog", "No input audio device selected.", None, QtGui.QApplication.UnicodeUTF8))
        self.grpBoxOutput.setTitle(QtGui.QApplication.translate("Dialog", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.outputDevice_lbl.setText(QtGui.QApplication.translate("Dialog", "No output audio device selected.", None, QtGui.QApplication.UnicodeUTF8))

