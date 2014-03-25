# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Graphic_Interface\UI Files\new_file_dialog.ui'
#
# Created: Thu Mar 20 01:10:28 2014
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NewFileDialog(object):
    def setupUi(self, NewFileDialog):
        NewFileDialog.setObjectName(_fromUtf8("NewFileDialog"))
        NewFileDialog.resize(209, 158)
        self.formLayout = QtGui.QFormLayout(NewFileDialog)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.sbxSamplingRate = QtGui.QSpinBox(NewFileDialog)
        self.sbxSamplingRate.setMinimum(1)
        self.sbxSamplingRate.setMaximum(1000000000)
        self.sbxSamplingRate.setProperty("value", 44100)
        self.sbxSamplingRate.setObjectName(_fromUtf8("sbxSamplingRate"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.sbxSamplingRate)
        self.label_2 = QtGui.QLabel(NewFileDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.dsbxDuration = QtGui.QDoubleSpinBox(NewFileDialog)
        self.dsbxDuration.setMaximum(3600.0)
        self.dsbxDuration.setProperty("value", 5.0)
        self.dsbxDuration.setObjectName(_fromUtf8("dsbxDuration"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.dsbxDuration)
        self.label = QtGui.QLabel(NewFileDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.label_3 = QtGui.QLabel(NewFileDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.rbtnSilence = QtGui.QRadioButton(NewFileDialog)
        self.rbtnSilence.setChecked(True)
        self.rbtnSilence.setObjectName(_fromUtf8("rbtnSilence"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.rbtnSilence)
        self.rbtnWhiteNoise = QtGui.QRadioButton(NewFileDialog)
        self.rbtnWhiteNoise.setObjectName(_fromUtf8("rbtnWhiteNoise"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.rbtnWhiteNoise)
        self.buttonBox = QtGui.QDialogButtonBox(NewFileDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.SpanningRole, self.buttonBox)
        self.cbxBitDepth = QtGui.QComboBox(NewFileDialog)
        self.cbxBitDepth.setObjectName(_fromUtf8("cbxBitDepth"))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cbxBitDepth)

        self.retranslateUi(NewFileDialog)
        self.cbxBitDepth.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewFileDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewFileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewFileDialog)

    def retranslateUi(self, NewFileDialog):
        NewFileDialog.setWindowTitle(QtGui.QApplication.translate("NewFileDialog", "New file", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setSuffix(QtGui.QApplication.translate("NewFileDialog", " Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewFileDialog", "Duration:", None, QtGui.QApplication.UnicodeUTF8))
        self.dsbxDuration.setSuffix(QtGui.QApplication.translate("NewFileDialog", " sec", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewFileDialog", "Sampling rate:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewFileDialog", "Bit depth:", None, QtGui.QApplication.UnicodeUTF8))
        self.rbtnSilence.setText(QtGui.QApplication.translate("NewFileDialog", "Silence", None, QtGui.QApplication.UnicodeUTF8))
        self.rbtnWhiteNoise.setText(QtGui.QApplication.translate("NewFileDialog", "White noise", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(0, QtGui.QApplication.translate("NewFileDialog", "8 bits", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(1, QtGui.QApplication.translate("NewFileDialog", "16 bits", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(2, QtGui.QApplication.translate("NewFileDialog", "32 bits", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(3, QtGui.QApplication.translate("NewFileDialog", "64 bits", None, QtGui.QApplication.UnicodeUTF8))

