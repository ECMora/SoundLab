# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\dev\duetto\d-SoundLab\duetto-SoundLab\graphic_interface\UI_Files\new_file_dialog.ui'
#
# Created: Tue Dec 15 01:14:18 2015
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
        NewFileDialog.setWindowModality(QtCore.Qt.WindowModal)
        NewFileDialog.resize(199, 168)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewFileDialog.sizePolicy().hasHeightForWidth())
        NewFileDialog.setSizePolicy(sizePolicy)
        self.formLayout = QtGui.QFormLayout(NewFileDialog)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(-1, -1, -1, 6)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(NewFileDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
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
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.sbxSamplingRate)
        self.label_2 = QtGui.QLabel(NewFileDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.dsbxDuration = QtGui.QDoubleSpinBox(NewFileDialog)
        self.dsbxDuration.setSuffix(_fromUtf8(""))
        self.dsbxDuration.setMaximum(3600.0)
        self.dsbxDuration.setProperty("value", 5.0)
        self.dsbxDuration.setObjectName(_fromUtf8("dsbxDuration"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.dsbxDuration)
        self.label_3 = QtGui.QLabel(NewFileDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.cbxBitDepth = QtGui.QComboBox(NewFileDialog)
        self.cbxBitDepth.setEditable(False)
        self.cbxBitDepth.setObjectName(_fromUtf8("cbxBitDepth"))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.cbxBitDepth.addItem(_fromUtf8(""))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cbxBitDepth)
        self.groupBox = QtGui.QGroupBox(NewFileDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.rbtnSilence = QtGui.QRadioButton(self.groupBox)
        self.rbtnSilence.setGeometry(QtCore.QRect(10, 19, 71, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbtnSilence.sizePolicy().hasHeightForWidth())
        self.rbtnSilence.setSizePolicy(sizePolicy)
        self.rbtnSilence.setChecked(True)
        self.rbtnSilence.setObjectName(_fromUtf8("rbtnSilence"))
        self.rbtnWhiteNoise = QtGui.QRadioButton(self.groupBox)
        self.rbtnWhiteNoise.setGeometry(QtCore.QRect(85, 19, 91, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbtnWhiteNoise.sizePolicy().hasHeightForWidth())
        self.rbtnWhiteNoise.setSizePolicy(sizePolicy)
        self.rbtnWhiteNoise.setObjectName(_fromUtf8("rbtnWhiteNoise"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(NewFileDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(NewFileDialog)
        self.sbxSamplingRate.setCurrentIndex(3)
        self.cbxBitDepth.setCurrentIndex(2)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewFileDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewFileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewFileDialog)

    def retranslateUi(self, NewFileDialog):
        NewFileDialog.setWindowTitle(QtGui.QApplication.translate("NewFileDialog", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewFileDialog", "Sampling Rate (Hz):", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(0, QtGui.QApplication.translate("NewFileDialog", "22050", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(1, QtGui.QApplication.translate("NewFileDialog", "24000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(2, QtGui.QApplication.translate("NewFileDialog", "32000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(3, QtGui.QApplication.translate("NewFileDialog", "44100", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(4, QtGui.QApplication.translate("NewFileDialog", "96000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(5, QtGui.QApplication.translate("NewFileDialog", "100000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(6, QtGui.QApplication.translate("NewFileDialog", "125000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(7, QtGui.QApplication.translate("NewFileDialog", "150000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(8, QtGui.QApplication.translate("NewFileDialog", "192000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(9, QtGui.QApplication.translate("NewFileDialog", "200000", None, QtGui.QApplication.UnicodeUTF8))
        self.sbxSamplingRate.setItemText(10, QtGui.QApplication.translate("NewFileDialog", "250000", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewFileDialog", "Duration (s):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewFileDialog", "Bit Depth (bits):", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(0, QtGui.QApplication.translate("NewFileDialog", "8", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(1, QtGui.QApplication.translate("NewFileDialog", "12", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(2, QtGui.QApplication.translate("NewFileDialog", "16", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(3, QtGui.QApplication.translate("NewFileDialog", "24", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(4, QtGui.QApplication.translate("NewFileDialog", "32", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBitDepth.setItemText(5, QtGui.QApplication.translate("NewFileDialog", "64", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("NewFileDialog", " Content ", None, QtGui.QApplication.UnicodeUTF8))
        self.rbtnSilence.setText(QtGui.QApplication.translate("NewFileDialog", "Silence", None, QtGui.QApplication.UnicodeUTF8))
        self.rbtnWhiteNoise.setText(QtGui.QApplication.translate("NewFileDialog", "White Noise", None, QtGui.QApplication.UnicodeUTF8))

