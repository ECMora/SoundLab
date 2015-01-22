# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\duetto-SoundLab\graphic_interface\UI_Files\insertSilence.ui'
#
# Created: Mon Jan 05 10:29:01 2015
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
        Dialog.resize(190, 98)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.formLayout = QtGui.QFormLayout(Dialog)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.btonaceptar = QtGui.QPushButton(Dialog)
        self.btonaceptar.setToolTip(_fromUtf8(""))
        self.btonaceptar.setCheckable(False)
        self.btonaceptar.setDefault(False)
        self.btonaceptar.setFlat(False)
        self.btonaceptar.setObjectName(_fromUtf8("btonaceptar"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.btonaceptar)
        self.btoncancelar = QtGui.QPushButton(Dialog)
        self.btoncancelar.setToolTip(_fromUtf8(""))
        self.btoncancelar.setDefault(False)
        self.btoncancelar.setObjectName(_fromUtf8("btoncancelar"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.btoncancelar)
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label)
        self.insertSpinBox = QtGui.QSpinBox(Dialog)
        self.insertSpinBox.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.insertSpinBox.setMaximum(100000000)
        self.insertSpinBox.setProperty("value", 1000)
        self.insertSpinBox.setObjectName(_fromUtf8("insertSpinBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.insertSpinBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.btonaceptar, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QObject.connect(self.btoncancelar, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.btonaceptar.setText(QtGui.QApplication.translate("Dialog", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.btoncancelar.setText(QtGui.QApplication.translate("Dialog", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Select the duration", None, QtGui.QApplication.UnicodeUTF8))
        self.insertSpinBox.setSuffix(QtGui.QApplication.translate("Dialog", " ms", None, QtGui.QApplication.UnicodeUTF8))

