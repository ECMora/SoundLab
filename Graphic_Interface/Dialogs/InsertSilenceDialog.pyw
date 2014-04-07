# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Archivos graficos\insertSilence.ui'
#
# Created: Fri Aug 02 20:00:21 2013
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
        Dialog.resize(172, 134)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 181, 41))
        self.label.setObjectName(_fromUtf8("label"))
        self.insertSpinBox = QtGui.QSpinBox(Dialog)
        self.insertSpinBox.setGeometry(QtCore.QRect(10, 60, 151, 21))
        self.insertSpinBox.setMaximum(100000000)
        self.insertSpinBox.setProperty("value", 0)
        self.insertSpinBox.setObjectName(_fromUtf8("insertSpinBox"))
        self.btonaceptar = QtGui.QPushButton(Dialog)
        self.btonaceptar.setGeometry(QtCore.QRect(10, 100, 65, 23))
        self.btonaceptar.setToolTip(_fromUtf8(""))
        self.btonaceptar.setCheckable(False)
        self.btonaceptar.setDefault(False)
        self.btonaceptar.setFlat(False)
        self.btonaceptar.setObjectName(_fromUtf8("btonaceptar"))
        self.btoncancelar = QtGui.QPushButton(Dialog)
        self.btoncancelar.setGeometry(QtCore.QRect(100, 100, 65, 23))
        self.btoncancelar.setToolTip(_fromUtf8(""))
        self.btoncancelar.setDefault(False)
        self.btoncancelar.setObjectName(_fromUtf8("btoncancelar"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.btonaceptar, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QObject.connect(self.btoncancelar, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Options", None))
        self.label.setText(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600; color:#0000f7;\">Select the time interval </span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600; color:#0000f7;\">to be inserted (in ms)</span></p></body></html>", None))
        self.btonaceptar.setText(_translate("Dialog", "Aceptar", None))
        self.btoncancelar.setText(_translate("Dialog", "Cancelar", None))

