# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\duetto-SoundLab\graphic_interface\UI_Files\cross_correlationDialog.ui'
#
# Created: Fri Feb 20 14:45:58 2015
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_cross_correlationDialog(object):
    def setupUi(self, cross_correlationDialog):
        cross_correlationDialog.setObjectName(_fromUtf8("cross_correlationDialog"))
        cross_correlationDialog.resize(619, 290)
        self.gridLayout = QtGui.QGridLayout(cross_correlationDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.orderCheckBox = QtGui.QCheckBox(cross_correlationDialog)
        self.orderCheckBox.setObjectName(_fromUtf8("orderCheckBox"))
        self.gridLayout.addWidget(self.orderCheckBox, 2, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.oscillogramWidget = OscillogramWidget(cross_correlationDialog)
        self.oscillogramWidget.setStyleSheet(_fromUtf8("background-color: rgb(11, 64, 255);"))
        self.oscillogramWidget.setObjectName(_fromUtf8("oscillogramWidget"))
        self.verticalLayout.addWidget(self.oscillogramWidget)
        self.spectrogramWidget = SpectrogramWidget(cross_correlationDialog)
        self.spectrogramWidget.setStyleSheet(_fromUtf8("background-color: rgb(49, 8, 255);"))
        self.spectrogramWidget.setObjectName(_fromUtf8("spectrogramWidget"))
        self.verticalLayout.addWidget(self.spectrogramWidget)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.matchTableWidget = QtGui.QTableWidget(cross_correlationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.matchTableWidget.sizePolicy().hasHeightForWidth())
        self.matchTableWidget.setSizePolicy(sizePolicy)
        self.matchTableWidget.setMaximumSize(QtCore.QSize(350, 16777215))
        self.matchTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.matchTableWidget.setProperty("showDropIndicator", False)
        self.matchTableWidget.setDragDropOverwriteMode(False)
        self.matchTableWidget.setAlternatingRowColors(True)
        self.matchTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.matchTableWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.matchTableWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.matchTableWidget.setColumnCount(2)
        self.matchTableWidget.setObjectName(_fromUtf8("matchTableWidget"))
        self.matchTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.matchTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.matchTableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.matchTableWidget, 1, 1, 1, 1)

        self.retranslateUi(cross_correlationDialog)
        QtCore.QMetaObject.connectSlotsByName(cross_correlationDialog)

    def retranslateUi(self, cross_correlationDialog):
        cross_correlationDialog.setWindowTitle(QtGui.QApplication.translate("cross_correlationDialog", "Cross-correlation", None, QtGui.QApplication.UnicodeUTF8))
        self.orderCheckBox.setText(QtGui.QApplication.translate("cross_correlationDialog", "Order by match", None, QtGui.QApplication.UnicodeUTF8))
        item = self.matchTableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("cross_correlationDialog", "Match", None, QtGui.QApplication.UnicodeUTF8))
        item = self.matchTableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("cross_correlationDialog", "Offset", None, QtGui.QApplication.UnicodeUTF8))

from duetto.widgets.OscillogramWidget import OscillogramWidget
from duetto.widgets.SpectrogramWidget import SpectrogramWidget
