# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Biologia\DUETTO PROGRAMS\Sound Lab\DuettoSystem\graphic_interface\UI Files\Two_Dimensional_AnalisysWindowUI.ui'
#
# Created: Thu Jul 17 13:46:15 2014
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TwoDimensionalWindow(object):
    def setupUi(self, TwoDimensionalWindow):
        TwoDimensionalWindow.setObjectName(_fromUtf8("TwoDimensionalWindow"))
        TwoDimensionalWindow.resize(483, 377)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TwoDimensionalWindow.sizePolicy().hasHeightForWidth())
        TwoDimensionalWindow.setSizePolicy(sizePolicy)
        TwoDimensionalWindow.setMinimumSize(QtCore.QSize(0, 0))
        TwoDimensionalWindow.setSizeIncrement(QtCore.QSize(1, 1))
        self.centralwidget = QtGui.QWidget(TwoDimensionalWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = TwoDPlotWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout.addWidget(self.widget)
        TwoDimensionalWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(TwoDimensionalWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        TwoDimensionalWindow.setStatusBar(self.statusbar)
        self.dockGraphsOptions = QtGui.QDockWidget(TwoDimensionalWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockGraphsOptions.sizePolicy().hasHeightForWidth())
        self.dockGraphsOptions.setSizePolicy(sizePolicy)
        self.dockGraphsOptions.setObjectName(_fromUtf8("dockGraphsOptions"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.dockGraphsOptions.setWidget(self.dockWidgetContents)
        TwoDimensionalWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockGraphsOptions)
        self.actionHide_Show_Settings = QtGui.QAction(TwoDimensionalWindow)
        self.actionHide_Show_Settings.setObjectName(_fromUtf8("actionHide_Show_Settings"))
        self.actionSaveGraphImage = QtGui.QAction(TwoDimensionalWindow)
        self.actionSaveGraphImage.setObjectName(_fromUtf8("actionSaveGraphImage"))
        self.actionMark_Selected_Elements_As = QtGui.QAction(TwoDimensionalWindow)
        self.actionMark_Selected_Elements_As.setObjectName(_fromUtf8("actionMark_Selected_Elements_As"))

        self.retranslateUi(TwoDimensionalWindow)
        QtCore.QMetaObject.connectSlotsByName(TwoDimensionalWindow)

    def retranslateUi(self, TwoDimensionalWindow):
        TwoDimensionalWindow.setWindowTitle(QtGui.QApplication.translate("TwoDimensionalWindow", "Two Dimensional Analisys", None, QtGui.QApplication.UnicodeUTF8))
        self.dockGraphsOptions.setWindowTitle(QtGui.QApplication.translate("TwoDimensionalWindow", "Axis Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHide_Show_Settings.setText(QtGui.QApplication.translate("TwoDimensionalWindow", "Hide-Show Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHide_Show_Settings.setShortcut(QtGui.QApplication.translate("TwoDimensionalWindow", "Ctrl+Space", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveGraphImage.setText(QtGui.QApplication.translate("TwoDimensionalWindow", "Save Graph Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMark_Selected_Elements_As.setText(QtGui.QApplication.translate("TwoDimensionalWindow", "Mark Selected Elements As", None, QtGui.QApplication.UnicodeUTF8))

from graphic_interface.widgets.TwoDimensionalPlotWidget import TwoDPlotWidget
