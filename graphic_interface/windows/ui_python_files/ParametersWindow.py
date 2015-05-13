# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\duetto-SoundLab\graphic_interface\UI_Files\ParametersWindow.ui'
#
# Created: Wed May 13 15:58:10 2015
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(661, 388)
        MainWindow.setMinimumSize(QtCore.QSize(650, 0))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.save_bttn = QtGui.QPushButton(self.centralwidget)
        self.save_bttn.setObjectName(_fromUtf8("save_bttn"))
        self.gridLayout.addWidget(self.save_bttn, 3, 1, 1, 1)
        self.settings_widget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_widget.sizePolicy().hasHeightForWidth())
        self.settings_widget.setSizePolicy(sizePolicy)
        self.settings_widget.setMinimumSize(QtCore.QSize(250, 0))
        self.settings_widget.setMaximumSize(QtCore.QSize(400, 16777215))
        self.settings_widget.setObjectName(_fromUtf8("settings_widget"))
        self.gridLayout.addWidget(self.settings_widget, 2, 1, 1, 1)
        self.tab_parameters = QtGui.QTabWidget(self.centralwidget)
        self.tab_parameters.setObjectName(_fromUtf8("tab_parameters"))
        self.tab_time_parameters = QtGui.QWidget()
        self.tab_time_parameters.setObjectName(_fromUtf8("tab_time_parameters"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_time_parameters)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tab_parameters.addTab(self.tab_time_parameters, _fromUtf8(""))
        self.tab_wave_parameters = QtGui.QWidget()
        self.tab_wave_parameters.setObjectName(_fromUtf8("tab_wave_parameters"))
        self.tab_parameters.addTab(self.tab_wave_parameters, _fromUtf8(""))
        self.tab_spectral_params = QtGui.QWidget()
        self.tab_spectral_params.setObjectName(_fromUtf8("tab_spectral_params"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_spectral_params)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.parameter_locations_table = QtGui.QTableWidget(self.tab_spectral_params)
        self.parameter_locations_table.setObjectName(_fromUtf8("parameter_locations_table"))
        self.parameter_locations_table.setColumnCount(0)
        self.parameter_locations_table.setRowCount(0)
        self.gridLayout_2.addWidget(self.parameter_locations_table, 0, 1, 1, 1)
        self.tab_parameters.addTab(self.tab_spectral_params, _fromUtf8(""))
        self.gridLayout.addWidget(self.tab_parameters, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tab_parameters.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Parameters Configuration", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setToolTip(QtGui.QApplication.translate("MainWindow", "The batch window allow to execute a processing over multiples signal files.", None, QtGui.QApplication.UnicodeUTF8))
        self.save_bttn.setText(QtGui.QApplication.translate("MainWindow", "Save Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.tab_parameters.setTabText(self.tab_parameters.indexOf(self.tab_time_parameters), QtGui.QApplication.translate("MainWindow", "Time Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.tab_parameters.setTabText(self.tab_parameters.indexOf(self.tab_wave_parameters), QtGui.QApplication.translate("MainWindow", "Wave Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.tab_parameters.setTabText(self.tab_parameters.indexOf(self.tab_spectral_params), QtGui.QApplication.translate("MainWindow", "Spectral Parameters", None, QtGui.QApplication.UnicodeUTF8))

