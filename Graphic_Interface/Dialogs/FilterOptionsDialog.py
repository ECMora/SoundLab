# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Biologia\SISTEMA\DuettoSystem\Graphic_Interface\UI Files\FilterOptionsDialog.ui'
#
# Created: Fri Apr 25 12:05:13 2014
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
        Dialog.resize(315, 272)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btonaceptar = QtGui.QPushButton(Dialog)
        self.btonaceptar.setToolTip(_fromUtf8(""))
        self.btonaceptar.setCheckable(False)
        self.btonaceptar.setDefault(False)
        self.btonaceptar.setFlat(False)
        self.btonaceptar.setObjectName(_fromUtf8("btonaceptar"))
        self.gridLayout_2.addWidget(self.btonaceptar, 2, 1, 1, 1)
        self.btoncancelar = QtGui.QPushButton(Dialog)
        self.btoncancelar.setToolTip(_fromUtf8(""))
        self.btoncancelar.setDefault(False)
        self.btoncancelar.setObjectName(_fromUtf8("btoncancelar"))
        self.gridLayout_2.addWidget(self.btoncancelar, 2, 2, 1, 1)
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
        self.label_4 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_4.setIndent(4)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 3, 1, 1)
        self.spinBoxLowPass = QtGui.QSpinBox(self.groupBox)
        self.spinBoxLowPass.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.spinBoxLowPass.setMaximum(10000000)
        self.spinBoxLowPass.setObjectName(_fromUtf8("spinBoxLowPass"))
        self.gridLayout.addWidget(self.spinBoxLowPass, 0, 2, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_12.setIndent(14)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 3, 1, 1, 1)
        self.spinBoxBandPassFu = QtGui.QSpinBox(self.groupBox)
        self.spinBoxBandPassFu.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.spinBoxBandPassFu.setMaximum(10000000)
        self.spinBoxBandPassFu.setObjectName(_fromUtf8("spinBoxBandPassFu"))
        self.gridLayout.addWidget(self.spinBoxBandPassFu, 3, 2, 1, 1)
        self.rButtonBandPass = QtGui.QRadioButton(self.groupBox)
        self.rButtonBandPass.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rButtonBandPass.setObjectName(_fromUtf8("rButtonBandPass"))
        self.gridLayout.addWidget(self.rButtonBandPass, 2, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_8.setIndent(14)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 0, 1, 1, 1)
        self.rButtonLowPass = QtGui.QRadioButton(self.groupBox)
        self.rButtonLowPass.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rButtonLowPass.setObjectName(_fromUtf8("rButtonLowPass"))
        self.gridLayout.addWidget(self.rButtonLowPass, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_2.setIndent(4)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)
        self.spinBoxHighPass = QtGui.QSpinBox(self.groupBox)
        self.spinBoxHighPass.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.spinBoxHighPass.setMaximum(10000000)
        self.spinBoxHighPass.setObjectName(_fromUtf8("spinBoxHighPass"))
        self.gridLayout.addWidget(self.spinBoxHighPass, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_3.setIndent(4)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 3, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label.setIndent(4)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)
        self.spinBoxBandStopFu = QtGui.QSpinBox(self.groupBox)
        self.spinBoxBandStopFu.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.spinBoxBandStopFu.setMaximum(10000000)
        self.spinBoxBandStopFu.setObjectName(_fromUtf8("spinBoxBandStopFu"))
        self.gridLayout.addWidget(self.spinBoxBandStopFu, 5, 2, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_6.setIndent(4)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 3, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_7.setIndent(14)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 5, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_5.setIndent(4)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 3, 1, 1)
        self.rButtonBandStop = QtGui.QRadioButton(self.groupBox)
        self.rButtonBandStop.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rButtonBandStop.setObjectName(_fromUtf8("rButtonBandStop"))
        self.gridLayout.addWidget(self.rButtonBandStop, 4, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_10.setIndent(14)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 1, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_11.setIndent(14)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 2, 1, 1, 1)
        self.spinBoxBandStopFl = QtGui.QSpinBox(self.groupBox)
        self.spinBoxBandStopFl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.spinBoxBandStopFl.setMaximum(10000000)
        self.spinBoxBandStopFl.setObjectName(_fromUtf8("spinBoxBandStopFl"))
        self.gridLayout.addWidget(self.spinBoxBandStopFl, 4, 2, 1, 1)
        self.rButtonHighPass = QtGui.QRadioButton(self.groupBox)
        self.rButtonHighPass.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.rButtonHighPass.setObjectName(_fromUtf8("rButtonHighPass"))
        self.gridLayout.addWidget(self.rButtonHighPass, 1, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_9.setIndent(14)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 4, 1, 1, 1)
        self.spinBoxBandPassFl = QtGui.QSpinBox(self.groupBox)
        self.spinBoxBandPassFl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.spinBoxBandPassFl.setMaximum(10000000)
        self.spinBoxBandPassFl.setObjectName(_fromUtf8("spinBoxBandPassFl"))
        self.gridLayout.addWidget(self.spinBoxBandPassFl, 2, 2, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.btonaceptar, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QObject.connect(self.btoncancelar, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Filter Options", None, QtGui.QApplication.UnicodeUTF8))
        self.btonaceptar.setText(QtGui.QApplication.translate("Dialog", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.btoncancelar.setText(QtGui.QApplication.translate("Dialog", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Select the filter frecuency", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "Fu", None, QtGui.QApplication.UnicodeUTF8))
        self.rButtonBandPass.setText(QtGui.QApplication.translate("Dialog", "Band Pass", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "Fc", None, QtGui.QApplication.UnicodeUTF8))
        self.rButtonLowPass.setText(QtGui.QApplication.translate("Dialog", "Low Pass", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Fu", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.rButtonBandStop.setText(QtGui.QApplication.translate("Dialog", "Band Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "Fc", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "Fl", None, QtGui.QApplication.UnicodeUTF8))
        self.rButtonHighPass.setText(QtGui.QApplication.translate("Dialog", "High Pass", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "Fl", None, QtGui.QApplication.UnicodeUTF8))

