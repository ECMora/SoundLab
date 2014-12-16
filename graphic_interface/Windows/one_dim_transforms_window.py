# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\DuettoSystem\graphic_interface\UI_Files\one_dim_transforms_window.ui'
#
# Created: Mon Dec 15 14:18:08 2014
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_OneDimensionalWindow(object):
    def setupUi(self, OneDimensionalWindow):
        OneDimensionalWindow.setObjectName(_fromUtf8("OneDimensionalWindow"))
        OneDimensionalWindow.resize(483, 377)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OneDimensionalWindow.sizePolicy().hasHeightForWidth())
        OneDimensionalWindow.setSizePolicy(sizePolicy)
        OneDimensionalWindow.setMinimumSize(QtCore.QSize(0, 0))
        OneDimensionalWindow.setSizeIncrement(QtCore.QSize(1, 1))
        self.centralwidget = QtGui.QWidget(OneDimensionalWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = OneDimPlotWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout.addWidget(self.widget)
        OneDimensionalWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(OneDimensionalWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        OneDimensionalWindow.setStatusBar(self.statusbar)
        self.dockSettings = QtGui.QDockWidget(OneDimensionalWindow)
        self.dockSettings.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockSettings.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockSettings.setObjectName(_fromUtf8("dockSettings"))
        self.dock_settings_contents = QtGui.QWidget()
        self.dock_settings_contents.setObjectName(_fromUtf8("dock_settings_contents"))
        self.dockSettings.setWidget(self.dock_settings_contents)
        OneDimensionalWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockSettings)

        self.retranslateUi(OneDimensionalWindow)
        QtCore.QMetaObject.connectSlotsByName(OneDimensionalWindow)

    def retranslateUi(self, OneDimensionalWindow):
        OneDimensionalWindow.setWindowTitle(QtGui.QApplication.translate("OneDimensionalWindow", "One Dimensional Functions", None, QtGui.QApplication.UnicodeUTF8))
        self.dockSettings.setWindowTitle(QtGui.QApplication.translate("OneDimensionalWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))

from ..widgets.OneDimensionalPlotWidget import OneDimPlotWidget
import icons_rc
