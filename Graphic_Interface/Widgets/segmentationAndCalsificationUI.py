# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Graphic_Interface\UI Files\SegmentationAndClasificationWindow.ui'
#
# Created: Sat Feb 01 12:43:51 2014
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(725, 421)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(641, 0))
        self.centralwidget.setMaximumSize(QtCore.QSize(1300, 900))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget = QSignalVisualizerWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 725, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuArchivo = QtGui.QMenu(self.menubar)
        self.menuArchivo.setObjectName(_fromUtf8("menuArchivo"))
        self.menuDetection = QtGui.QMenu(self.menubar)
        self.menuDetection.setObjectName(_fromUtf8("menuDetection"))
        self.menuClasification = QtGui.QMenu(self.menubar)
        self.menuClasification.setObjectName(_fromUtf8("menuClasification"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionExportar = QtGui.QAction(MainWindow)
        self.actionExportar.setObjectName(_fromUtf8("actionExportar"))
        self.actionImportar = QtGui.QAction(MainWindow)
        self.actionImportar.setObjectName(_fromUtf8("actionImportar"))
        self.actionGuardar_Como = QtGui.QAction(MainWindow)
        self.actionGuardar_Como.setObjectName(_fromUtf8("actionGuardar_Como"))
        self.actionSalir = QtGui.QAction(MainWindow)
        self.actionSalir.setObjectName(_fromUtf8("actionSalir"))
        self.actionOscilogram_Detection = QtGui.QAction(MainWindow)
        self.actionOscilogram_Detection.setObjectName(_fromUtf8("actionOscilogram_Detection"))
        self.actionEspectrogram_Detection = QtGui.QAction(MainWindow)
        self.actionEspectrogram_Detection.setObjectName(_fromUtf8("actionEspectrogram_Detection"))
        self.actionParameters_Measurement = QtGui.QAction(MainWindow)
        self.actionParameters_Measurement.setObjectName(_fromUtf8("actionParameters_Measurement"))
        self.actionSegment_Agrupation = QtGui.QAction(MainWindow)
        self.actionSegment_Agrupation.setObjectName(_fromUtf8("actionSegment_Agrupation"))
        self.actionClear_Cursors = QtGui.QAction(MainWindow)
        self.actionClear_Cursors.setObjectName(_fromUtf8("actionClear_Cursors"))
        self.menuArchivo.addAction(self.actionExportar)
        self.menuArchivo.addAction(self.actionImportar)
        self.menuArchivo.addAction(self.actionGuardar_Como)
        self.menuArchivo.addAction(self.actionSalir)
        self.menuDetection.addAction(self.actionOscilogram_Detection)
        self.menuDetection.addAction(self.actionEspectrogram_Detection)
        self.menuDetection.addAction(self.actionClear_Cursors)
        self.menuDetection.addSeparator()
        self.menuDetection.addAction(self.actionParameters_Measurement)
        self.menuDetection.addSeparator()
        self.menuDetection.addAction(self.actionSegment_Agrupation)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuDetection.menuAction())
        self.menubar.addAction(self.menuClasification.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Duetto Sound Lab - Segmentation And Clasification Window ", None))
        self.menuArchivo.setTitle(_translate("MainWindow", "File", None))
        self.menuDetection.setTitle(_translate("MainWindow", "Detection", None))
        self.menuClasification.setTitle(_translate("MainWindow", "Clasification", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionExportar.setText(_translate("MainWindow", "Export", None))
        self.actionImportar.setText(_translate("MainWindow", "Import", None))
        self.actionGuardar_Como.setText(_translate("MainWindow", "Save As", None))
        self.actionSalir.setText(_translate("MainWindow", "Exit", None))
        self.actionOscilogram_Detection.setText(_translate("MainWindow", "Oscilogram Detection", None))
        self.actionEspectrogram_Detection.setText(_translate("MainWindow", "Spectrogram Detection", None))
        self.actionParameters_Measurement.setText(_translate("MainWindow", "Parameters Measurement", None))
        self.actionSegment_Agrupation.setText(_translate("MainWindow", "Segmentation", None))
        self.actionClear_Cursors.setText(_translate("MainWindow", "Clear Cursors", None))

from Graphic_Interface.Widgets.QSignalVisualizerWidget import QSignalVisualizerWidget
