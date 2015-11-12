# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\duetto-SoundLab\graphic_interface\UI_Files\new_file_dialog.ui'
#
# Created: Tue Nov 10 16:35:17 2015
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
        NewFileDialog.resize(234, 155)
        self.formLayout = QtGui.QFormLayout(NewFileDialog)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(NewFileDialog)
        self.label_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.dsbxDuration = QtGui.QDoubleSpinBox(NewFileDialog)
        self.dsbxDuration.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.dsbxDuration.setMaximum(3600.0)
        self.dsbxDuration.setProperty("value", 5.0)
        self.dsbxDuration.setObjectName(_fromUtf8("dsbxDuration"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.dsbxDuration)
        self.label = QtGui.QLabel(NewFileDialog)
        self.label.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.label_3 = QtGui.QLabel(NewFileDialog)
        self.label_3.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.rbtnSilence = QtGui.QRadioButton(NewFileDialog)
        self.rbtnSilence.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rbtnSilence.setChecked(True)
        self.rbtnSilence.setObjectName(_fromUtf8("rbtnSilence"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.rbtnSilence)
        self.rbtnWhiteNoise = QtGui.QRadioButton(NewFileDialog)
        self.rbtnWhiteNoise.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rbtnWhiteNoise.setObjectName(_fromUtf8("rbtnWhiteNoise"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.rbtnWhiteNoise)
        self.buttonBox = QtGui.QDialogButtonBox(NewFileDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.SpanningRole, self.buttonBox)
        self.cbxBitDepth = QtGui.QComboBox(NewFileDialog)
        self.cbxBitDepth.setEditable(False)
        self.cbxBitDepth.setObjectName(_fromUtf8("cbxBitDepth"))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cbxBitDepth)
        self.sbxSamplingRate = QtGui.QComboBox(NewFileDialog)
        self.sbxSamplingRate.setEditable(True)
        self.sbxSamplingRate.setObjectName(_fromUtf8("sbxSamplingRate"))
        self.sbxSamplingRate.addItem(_fromUtf8(""))
        self.sbxSamplingRate.addItem(_fromUtf8(""))
        self.sbxSamplingRate.addItem(_fromUtf8(""))
        self.sbxSamplingRate.addItem(_fromUtf8(""))
        self.sbxSamplingRate.addItem(_fromUtf8(""))
        self.sbxSamplingRate.addItem(_fromUtf8(""))
        self.sbxSamplingRate.addItem(_fromUtf8(""))
        self.sbxSamplingRate.addItem(_fromUtf8(""))
        self.sbxSamplingRate.addItem(_fromUtf8(""))
        self.sbxSamplingRate.addItem(_fromUtf8(""))
        self.sbxSamplingRate.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.sbxSamplingRate)

        self.retranslateUi(NewFileDialog)
        self.cbxBitDepth.setCurrentIndex(0)
        self.sbxSamplingRate.setCurrentIndex(1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewFileDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewFileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewFileDialog)

    def retranslateUi(self, NewFileDialog):
        NewFileDialog.setWindowTitle(QtGui.QApplication.translate("NewFileDialog", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewFileDialog", "Duration:", None, QtGui.QApplication.UnicodeUTF8))
        self.dsbxDuration.setSuffix(QtGui.QApplication.translate("NewFileDialog", " sec", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewFileDialog", "Sampling Rate kHz:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewFileDialog", "Bit Depth:", None, QtGui.QApplication.UnicodeUTF8))
        self.rbtnSilence.setText(QtGui.QApplication.translate("NewFileDialog", "Silence", None, QtGui.QApplication.UnicodeUTF8))
        self.rbtnWhiteNoise.setText(QtGui.QApplication.translate("NewFileDialog", "White Noise", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(0, QtGui.QApplication.translate("NewFileDialog", "8 bits", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(1, QtGui.QApplication.translate("NewFileDialog", "12", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(2, QtGui.QApplication.translate("NewFileDialog", "16", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(3, QtGui.QApplication.translate("NewFileDialog", "24", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(4, QtGui.QApplication.translate("NewFileDialog", "32", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(0, QtGui.QApplication.translate("NewFileDialog", "22050", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(1, QtGui.QApplication.translate("NewFileDialog", "44100", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(2, QtGui.QApplication.translate("NewFileDialog", "24000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(3, QtGui.QApplication.translate("NewFileDialog", "32000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(4, QtGui.QApplication.translate("NewFileDialog", "96000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(5, QtGui.QApplication.translate("NewFileDialog", "100000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(6, QtGui.QApplication.translate("NewFileDialog", "125000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(7, QtGui.QApplication.translate("NewFileDialog", "150000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(8, QtGui.QApplication.translate("NewFileDialog", "192000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(9, QtGui.QApplication.translate("NewFileDialog", "200000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(10, QtGui.QApplication.translate("NewFileDialog", "250000", None, QtGui.QApplication.UnicodeUTF8))

