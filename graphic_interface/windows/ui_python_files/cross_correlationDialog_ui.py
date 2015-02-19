# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphic_interface\UI_Files\cross_correlationDialog.ui'
#
# Created: Wed Feb 18 12:54:45 2015
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
        cross_correlationDialog.resize(475, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(cross_correlationDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.oscillogramWidget = OscillogramWidget(cross_correlationDialog)
        self.oscillogramWidget.setObjectName(_fromUtf8("oscillogramWidget"))
        self.verticalLayout_4.addWidget(self.oscillogramWidget)
        self.spectrogramWidget = SpectrogramWidget(cross_correlationDialog)
        self.spectrogramWidget.setObjectName(_fromUtf8("spectrogramWidget"))
        self.verticalLayout_4.addWidget(self.spectrogramWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.matchTableWidget = QtGui.QTableWidget(cross_correlationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.matchTableWidget.sizePolicy().hasHeightForWidth())
        self.matchTableWidget.setSizePolicy(sizePolicy)
        self.matchTableWidget.setMaximumSize(QtCore.QSize(150, 16777215))
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
        self.verticalLayout.addWidget(self.matchTableWidget)
        self.groupBox = QtGui.QGroupBox(cross_correlationDialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.orderCheckBox = QtGui.QCheckBox(self.groupBox)
        self.orderCheckBox.setObjectName(_fromUtf8("orderCheckBox"))
        self.verticalLayout_2.addWidget(self.orderCheckBox)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(cross_correlationDialog)
        QtCore.QMetaObject.connectSlotsByName(cross_correlationDialog)

    def retranslateUi(self, cross_correlationDialog):
        cross_correlationDialog.setWindowTitle(QtGui.QApplication.translate("cross_correlationDialog", "Cross-correlation", None, QtGui.QApplication.UnicodeUTF8))
        item = self.matchTableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("cross_correlationDialog", "Match", None, QtGui.QApplication.UnicodeUTF8))
        item = self.matchTableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("cross_correlationDialog", "Offset", None, QtGui.QApplication.UnicodeUTF8))
        self.orderCheckBox.setText(QtGui.QApplication.translate("cross_correlationDialog", "Order by match", None, QtGui.QApplication.UnicodeUTF8))

from duetto.widgets.OscillogramWidget import OscillogramWidget
from duetto.widgets.SpectrogramWidget import SpectrogramWidget
