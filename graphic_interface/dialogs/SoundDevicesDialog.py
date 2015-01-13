# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SoundDevicesDialog.ui'
#
# Created: Fri Jan 09 23:07:58 2015
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
        Dialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.grpBoxInput = QtGui.QGroupBox(Dialog)
        self.grpBoxInput.setObjectName(_fromUtf8("grpBoxInput"))
        self.gridLayout.addWidget(self.grpBoxInput, 0, 0, 1, 1)
        self.grpBoxOutput = QtGui.QGroupBox(Dialog)
        self.grpBoxOutput.setObjectName(_fromUtf8("grpBoxOutput"))
        self.gridLayout.addWidget(self.grpBoxOutput, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Sound Devices", None, QtGui.QApplication.UnicodeUTF8))
        self.grpBoxInput.setTitle(QtGui.QApplication.translate("Dialog", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.grpBoxOutput.setTitle(QtGui.QApplication.translate("Dialog", "Output", None, QtGui.QApplication.UnicodeUTF8))

