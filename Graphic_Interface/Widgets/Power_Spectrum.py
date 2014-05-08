# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Gaby\Desktop\DuettoSystem\Graphic_Interface\UI Files\power_spectrum.ui'
#
# Created: Thu May 08 11:36:09 2014
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PowSpecWindow(object):
    def setupUi(self, PowSpecWindow):
        PowSpecWindow.setObjectName(_fromUtf8("PowSpecWindow"))
        PowSpecWindow.resize(483, 377)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PowSpecWindow.sizePolicy().hasHeightForWidth())
        PowSpecWindow.setSizePolicy(sizePolicy)
        PowSpecWindow.setMinimumSize(QtCore.QSize(0, 0))
        PowSpecWindow.setSizeIncrement(QtCore.QSize(1, 1))
        self.centralwidget = QtGui.QWidget(PowSpecWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = PowSpecPlotWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout.addWidget(self.widget)
        PowSpecWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(PowSpecWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PowSpecWindow.setStatusBar(self.statusbar)
        self.actionHighest_frequency = QtGui.QAction(PowSpecWindow)
        self.actionHighest_frequency.setObjectName(_fromUtf8("actionHighest_frequency"))

        self.retranslateUi(PowSpecWindow)
        QtCore.QMetaObject.connectSlotsByName(PowSpecWindow)

    def retranslateUi(self, PowSpecWindow):
        PowSpecWindow.setWindowTitle(QtGui.QApplication.translate("PowSpecWindow", "Power Spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHighest_frequency.setText(QtGui.QApplication.translate("PowSpecWindow", "Highest frequency", None, QtGui.QApplication.UnicodeUTF8))

from PowSpecPlotWidget import PowSpecPlotWidget
