# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'power_spectrum.ui'
#
# Created: Tue Jul 08 12:35:54 2014
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
        self.toolBar = QtGui.QToolBar(PowSpecWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        PowSpecWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockSettings = QtGui.QDockWidget(PowSpecWindow)
        self.dockSettings.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockSettings.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockSettings.setObjectName(_fromUtf8("dockSettings"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.dockSettings.setWidget(self.dockWidgetContents)
        PowSpecWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockSettings)
        self.actionOneDimFunctSettings = QtGui.QAction(PowSpecWindow)
        self.actionOneDimFunctSettings.setObjectName(_fromUtf8("actionOneDimFunctSettings"))
        self.toolBar.addAction(self.actionOneDimFunctSettings)

        self.retranslateUi(PowSpecWindow)
        QtCore.QMetaObject.connectSlotsByName(PowSpecWindow)

    def retranslateUi(self, PowSpecWindow):
        PowSpecWindow.setWindowTitle(QtGui.QApplication.translate("PowSpecWindow", "One Dimensional Functions", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("PowSpecWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.dockSettings.setWindowTitle(QtGui.QApplication.translate("PowSpecWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOneDimFunctSettings.setText(QtGui.QApplication.translate("PowSpecWindow", "OneDimFunctSettings", None, QtGui.QApplication.UnicodeUTF8))

from PowSpecPlotWidget import PowSpecPlotWidget
