# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_elemDetectSettings.ui'
#
# Created: Wed Jul 16 16:49:36 2014
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
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(1100, 660)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(1100, 660))
        Dialog.setMaximumSize(QtCore.QSize(1100, 664))
        Dialog.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:pad, x1:0.006, y1:0.017, x2:0.886, y2:0.892045, stop:0.0340909 rgba(94, 116, 236, 255), stop:1 rgba(255, 255, 255, 255));\n"
"font: 75 10pt \"MS Shell Dlg 2\";"))
        Dialog.setModal(False)
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.widget = QSignalDetectorWidget(Dialog)
        self.widget.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout_5 = QtGui.QFormLayout(self.widget)
        self.formLayout_5.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)
        self.dock_settings = QtGui.QDockWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_settings.sizePolicy().hasHeightForWidth())
        self.dock_settings.setSizePolicy(sizePolicy)
        self.dock_settings.setMinimumSize(QtCore.QSize(250, 84))
        self.dock_settings.setMaximumSize(QtCore.QSize(250, 524287))
        self.dock_settings.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.dock_settings.setFloating(False)
        self.dock_settings.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.dock_settings.setWindowTitle(_fromUtf8(""))
        self.dock_settings.setObjectName(_fromUtf8("dock_settings"))
        self.osc_settings_contents = QtGui.QWidget()
        self.osc_settings_contents.setObjectName(_fromUtf8("osc_settings_contents"))
        self.dock_settings.setWidget(self.osc_settings_contents)
        self.gridLayout_3.addWidget(self.dock_settings, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStyleSheet(_fromUtf8("font: 75 11pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(8, 100, 180);\n"
"color: rgb(255, 255, 255);"))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Detection Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.widget.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Signal to learn about algorithm parameters</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

from Graphic_Interface.Widgets.QSignalDetectorWidget import QSignalDetectorWidget
