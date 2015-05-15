# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\duetto-SoundLab\graphic_interface\UI_Files\ParametersWindow.ui'
#
# Created: Fri May 15 14:48:36 2015
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
        Dialog.resize(604, 430)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tab_parameters = QtGui.QTabWidget(Dialog)
        self.tab_parameters.setMinimumSize(QtCore.QSize(400, 0))
        self.tab_parameters.setObjectName(_fromUtf8("tab_parameters"))
        self.tab_time_parameters = QtGui.QWidget()
        self.tab_time_parameters.setObjectName(_fromUtf8("tab_time_parameters"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_time_parameters)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.time_parameter_table = QtGui.QTableWidget(self.tab_time_parameters)
        self.time_parameter_table.setObjectName(_fromUtf8("time_parameter_table"))
        self.time_parameter_table.setColumnCount(0)
        self.time_parameter_table.setRowCount(0)
        self.gridLayout_3.addWidget(self.time_parameter_table, 0, 0, 1, 1)
        self.tab_parameters.addTab(self.tab_time_parameters, _fromUtf8(""))
        self.tab_wave_parameters = QtGui.QWidget()
        self.tab_wave_parameters.setObjectName(_fromUtf8("tab_wave_parameters"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab_wave_parameters)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.wave_parameter_table = QtGui.QTableWidget(self.tab_wave_parameters)
        self.wave_parameter_table.setObjectName(_fromUtf8("wave_parameter_table"))
        self.wave_parameter_table.setColumnCount(0)
        self.wave_parameter_table.setRowCount(0)
        self.gridLayout_4.addWidget(self.wave_parameter_table, 0, 0, 1, 1)
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
        self.gridLayout.addWidget(self.tab_parameters, 0, 0, 3, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1)
        self.settings_widget = QtGui.QWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_widget.sizePolicy().hasHeightForWidth())
        self.settings_widget.setSizePolicy(sizePolicy)
        self.settings_widget.setMinimumSize(QtCore.QSize(180, 0))
        self.settings_widget.setMaximumSize(QtCore.QSize(400, 16777215))
        self.settings_widget.setObjectName(_fromUtf8("settings_widget"))
        self.gridLayout.addWidget(self.settings_widget, 0, 2, 3, 1)

        self.retranslateUi(Dialog)
        self.tab_parameters.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.tab_parameters.setTabText(self.tab_parameters.indexOf(self.tab_time_parameters), QtGui.QApplication.translate("Dialog", "Time Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.tab_parameters.setTabText(self.tab_parameters.indexOf(self.tab_wave_parameters), QtGui.QApplication.translate("Dialog", "Wave Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.tab_parameters.setTabText(self.tab_parameters.indexOf(self.tab_spectral_params), QtGui.QApplication.translate("Dialog", "Spectral Parameters", None, QtGui.QApplication.UnicodeUTF8))

