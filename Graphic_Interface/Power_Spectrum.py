# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'power_spectrum.ui'
#
# Created: Wed Nov 27 21:41:03 2013
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
        PowSpecWindow.resize(809, 607)
        self.centralwidget = QtGui.QWidget(PowSpecWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pow_spec = pow_plot(self.centralwidget)
        self.pow_spec.setObjectName(_fromUtf8("pow_spec"))
        self.verticalLayout.addWidget(self.pow_spec)
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

from wdoscilogram import pow_plot
