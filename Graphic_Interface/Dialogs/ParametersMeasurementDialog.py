# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Biologia\SISTEMA\DuettoSystemYasel\Graphic_Interface\UI Files\ParameterMeasurementDialogUI.ui'
#
# Created: Tue Mar 04 12:10:00 2014
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

class Ui_ParameterMeasurement(object):
    def setupUi(self, ParameterMeasurement):
        ParameterMeasurement.setObjectName(_fromUtf8("ParameterMeasurement"))
        ParameterMeasurement.resize(484, 404)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ParameterMeasurement.sizePolicy().hasHeightForWidth())
        ParameterMeasurement.setSizePolicy(sizePolicy)
        ParameterMeasurement.setSizeGripEnabled(False)
        self.gridLayout_3 = QtGui.QGridLayout(ParameterMeasurement)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(ParameterMeasurement)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabOscParam = QtGui.QWidget()
        self.tabOscParam.setObjectName(_fromUtf8("tabOscParam"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabOscParam)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gboxSpectralParameters = QtGui.QGroupBox(self.tabOscParam)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gboxSpectralParameters.sizePolicy().hasHeightForWidth())
        self.gboxSpectralParameters.setSizePolicy(sizePolicy)
        self.gboxSpectralParameters.setObjectName(_fromUtf8("gboxSpectralParameters"))
        self.gridLayout_4 = QtGui.QGridLayout(self.gboxSpectralParameters)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cbxPeakFreq = QtGui.QCheckBox(self.gboxSpectralParameters)
        self.cbxPeakFreq.setChecked(True)
        self.cbxPeakFreq.setObjectName(_fromUtf8("cbxPeakFreq"))
        self.gridLayout.addWidget(self.cbxPeakFreq, 0, 0, 1, 1)
        self.cbxEntropy = QtGui.QCheckBox(self.gboxSpectralParameters)
        self.cbxEntropy.setChecked(True)
        self.cbxEntropy.setObjectName(_fromUtf8("cbxEntropy"))
        self.gridLayout.addWidget(self.cbxEntropy, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.gboxSpectralParameters)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.gboxSpectralParameters, 1, 0, 1, 1)
        self.gboxOscilogramParameters = QtGui.QGroupBox(self.tabOscParam)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gboxOscilogramParameters.sizePolicy().hasHeightForWidth())
        self.gboxOscilogramParameters.setSizePolicy(sizePolicy)
        self.gboxOscilogramParameters.setObjectName(_fromUtf8("gboxOscilogramParameters"))
        self.gridLayout_5 = QtGui.QGridLayout(self.gboxOscilogramParameters)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.grdLyTemporalParameters = QtGui.QGridLayout()
        self.grdLyTemporalParameters.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.grdLyTemporalParameters.setSpacing(2)
        self.grdLyTemporalParameters.setObjectName(_fromUtf8("grdLyTemporalParameters"))
        self.cbxDistancefromStartToMax = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxDistancefromStartToMax.setChecked(True)
        self.cbxDistancefromStartToMax.setObjectName(_fromUtf8("cbxDistancefromStartToMax"))
        self.grdLyTemporalParameters.addWidget(self.cbxDistancefromStartToMax, 2, 0, 1, 1)
        self.cbxEndTime = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxEndTime.setChecked(True)
        self.cbxEndTime.setObjectName(_fromUtf8("cbxEndTime"))
        self.grdLyTemporalParameters.addWidget(self.cbxEndTime, 1, 0, 1, 1)
        self.cbxStartTime = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxStartTime.setChecked(True)
        self.cbxStartTime.setObjectName(_fromUtf8("cbxStartTime"))
        self.grdLyTemporalParameters.addWidget(self.cbxStartTime, 0, 0, 1, 1)
        self.cbxPeekToPeek = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxPeekToPeek.setChecked(True)
        self.cbxPeekToPeek.setObjectName(_fromUtf8("cbxPeekToPeek"))
        self.grdLyTemporalParameters.addWidget(self.cbxPeekToPeek, 3, 0, 1, 1)
        self.cbxRms = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxRms.setChecked(True)
        self.cbxRms.setObjectName(_fromUtf8("cbxRms"))
        self.grdLyTemporalParameters.addWidget(self.cbxRms, 4, 0, 1, 1)
        self.gridLayout_5.addLayout(self.grdLyTemporalParameters, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.gboxOscilogramParameters, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabOscParam, _fromUtf8(""))
        self.tabSpecParam = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabSpecParam.sizePolicy().hasHeightForWidth())
        self.tabSpecParam.setSizePolicy(sizePolicy)
        self.tabSpecParam.setMaximumSize(QtCore.QSize(516, 358))
        self.tabSpecParam.setObjectName(_fromUtf8("tabSpecParam"))
        self.tabWidget.addTab(self.tabSpecParam, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ParameterMeasurement)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ParameterMeasurement.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ParameterMeasurement.reject)
        QtCore.QMetaObject.connectSlotsByName(ParameterMeasurement)

    def retranslateUi(self, ParameterMeasurement):
        ParameterMeasurement.setWindowTitle(_translate("ParameterMeasurement", "Parameter Measurement", None))
        self.gboxSpectralParameters.setTitle(_translate("ParameterMeasurement", "Spectral Parameters", None))
        self.cbxPeakFreq.setText(_translate("ParameterMeasurement", "Peak Frecuency", None))
        self.cbxEntropy.setText(_translate("ParameterMeasurement", "Entropy", None))
        self.gboxOscilogramParameters.setTitle(_translate("ParameterMeasurement", "Temporal Parameters", None))
        self.cbxDistancefromStartToMax.setText(_translate("ParameterMeasurement", "Distance from start to max (ms)", None))
        self.cbxEndTime.setText(_translate("ParameterMeasurement", "End Time (ms)", None))
        self.cbxStartTime.setText(_translate("ParameterMeasurement", "Start Time (ms)", None))
        self.cbxPeekToPeek.setText(_translate("ParameterMeasurement", "Peek to Peek Amplitude", None))
        self.cbxRms.setText(_translate("ParameterMeasurement", "RMS", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOscParam), _translate("ParameterMeasurement", "Oscilogram Meditions", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSpecParam), _translate("ParameterMeasurement", "Specgram Meditions", None))

