# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\duetto-SoundLab\graphic_interface\UI_Files\FilterOptionsDialog.ui'
#
# Created: Mon Dec 07 14:16:33 2015
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
        Dialog.resize(262, 277)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.spinBoxHighPass = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBoxHighPass.setMinimumSize(QtCore.QSize(80, 0))
        self.spinBoxHighPass.setSuffix(_fromUtf8(""))
        self.spinBoxHighPass.setMaximum(300.0)
        self.spinBoxHighPass.setSingleStep(0.1)
        self.spinBoxHighPass.setObjectName(_fromUtf8("spinBoxHighPass"))
        self.gridLayout.addWidget(self.spinBoxHighPass, 1, 2, 1, 1)
        self.rButtonBandStop = QtGui.QRadioButton(self.groupBox)
        self.rButtonBandStop.setStyleSheet(_fromUtf8(""))
        self.rButtonBandStop.setObjectName(_fromUtf8("rButtonBandStop"))
        self.gridLayout.addWidget(self.rButtonBandStop, 4, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet(_fromUtf8(""))
        self.label_9.setIndent(14)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 4, 1, 1, 1)
        self.rButtonHighPass = QtGui.QRadioButton(self.groupBox)
        self.rButtonHighPass.setStyleSheet(_fromUtf8(""))
        self.rButtonHighPass.setObjectName(_fromUtf8("rButtonHighPass"))
        self.gridLayout.addWidget(self.rButtonHighPass, 1, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet(_fromUtf8(""))
        self.label_8.setIndent(14)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 0, 1, 1, 1)
        self.rButtonLowPass = QtGui.QRadioButton(self.groupBox)
        self.rButtonLowPass.setStyleSheet(_fromUtf8(""))
        self.rButtonLowPass.setObjectName(_fromUtf8("rButtonLowPass"))
        self.gridLayout.addWidget(self.rButtonLowPass, 0, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet(_fromUtf8(""))
        self.label_7.setIndent(14)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 5, 1, 1, 1)
        self.rButtonBandPass = QtGui.QRadioButton(self.groupBox)
        self.rButtonBandPass.setStyleSheet(_fromUtf8(""))
        self.rButtonBandPass.setObjectName(_fromUtf8("rButtonBandPass"))
        self.gridLayout.addWidget(self.rButtonBandPass, 2, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet(_fromUtf8(""))
        self.label_11.setIndent(14)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 2, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet(_fromUtf8(""))
        self.label_10.setIndent(14)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 1, 1, 1, 1)
        self.spinBoxLowPass = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBoxLowPass.setMinimumSize(QtCore.QSize(80, 0))
        self.spinBoxLowPass.setSuffix(_fromUtf8(""))
        self.spinBoxLowPass.setMaximum(300.0)
        self.spinBoxLowPass.setSingleStep(0.1)
        self.spinBoxLowPass.setObjectName(_fromUtf8("spinBoxLowPass"))
        self.gridLayout.addWidget(self.spinBoxLowPass, 0, 2, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet(_fromUtf8(""))
        self.label_12.setIndent(14)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 3, 1, 1, 1)
        self.spinBoxBandPassFl = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBoxBandPassFl.setMinimumSize(QtCore.QSize(80, 0))
        self.spinBoxBandPassFl.setSuffix(_fromUtf8(""))
        self.spinBoxBandPassFl.setMaximum(300.0)
        self.spinBoxBandPassFl.setSingleStep(0.1)
        self.spinBoxBandPassFl.setObjectName(_fromUtf8("spinBoxBandPassFl"))
        self.gridLayout.addWidget(self.spinBoxBandPassFl, 2, 2, 1, 1)
        self.spinBoxBandPassFu = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBoxBandPassFu.setMinimumSize(QtCore.QSize(80, 0))
        self.spinBoxBandPassFu.setSuffix(_fromUtf8(""))
        self.spinBoxBandPassFu.setMaximum(300.0)
        self.spinBoxBandPassFu.setSingleStep(0.1)
        self.spinBoxBandPassFu.setObjectName(_fromUtf8("spinBoxBandPassFu"))
        self.gridLayout.addWidget(self.spinBoxBandPassFu, 3, 2, 1, 1)
        self.spinBoxBandStopFl = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBoxBandStopFl.setMinimumSize(QtCore.QSize(80, 0))
        self.spinBoxBandStopFl.setSuffix(_fromUtf8(""))
        self.spinBoxBandStopFl.setMaximum(300.0)
        self.spinBoxBandStopFl.setSingleStep(0.1)
        self.spinBoxBandStopFl.setObjectName(_fromUtf8("spinBoxBandStopFl"))
        self.gridLayout.addWidget(self.spinBoxBandStopFl, 4, 2, 1, 1)
        self.spinBoxBandStopFu = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBoxBandStopFu.setMinimumSize(QtCore.QSize(80, 0))
        self.spinBoxBandStopFu.setSuffix(_fromUtf8(""))
        self.spinBoxBandStopFu.setMaximum(300.0)
        self.spinBoxBandStopFu.setSingleStep(0.1)
        self.spinBoxBandStopFu.setObjectName(_fromUtf8("spinBoxBandStopFu"))
        self.gridLayout.addWidget(self.spinBoxBandStopFu, 5, 2, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Select the filter frecuency", None, QtGui.QApplication.UnicodeUTF8))
        self.rButtonBandStop.setText(QtGui.QApplication.translate("Dialog", "Band Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "Fl ( kHz )", None, QtGui.QApplication.UnicodeUTF8))
        self.rButtonHighPass.setText(QtGui.QApplication.translate("Dialog", "High Pass", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "Fc ( kHz )", None, QtGui.QApplication.UnicodeUTF8))
        self.rButtonLowPass.setText(QtGui.QApplication.translate("Dialog", "Low Pass", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Fu ( kHz )", None, QtGui.QApplication.UnicodeUTF8))
        self.rButtonBandPass.setText(QtGui.QApplication.translate("Dialog", "Band Pass", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "Fl ( kHz )", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "Fc ( kHz )", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "Fu ( kHz )", None, QtGui.QApplication.UnicodeUTF8))

