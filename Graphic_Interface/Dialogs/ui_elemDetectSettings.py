# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Biologia\SISTEMA\DuettoSystem\Graphic_Interface\UI Files\ui_elemDetectSettings.ui'
#
# Created: Sat Apr 05 21:50:29 2014
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(885, 628)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.dockWidgetEspgram = QtGui.QDockWidget(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetEspgram.sizePolicy().hasHeightForWidth())
        self.dockWidgetEspgram.setSizePolicy(sizePolicy)
        self.dockWidgetEspgram.setFloating(False)
        self.dockWidgetEspgram.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.dockWidgetEspgram.setObjectName(_fromUtf8("dockWidgetEspgram"))
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName(_fromUtf8("dockWidgetContents_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_8 = QtGui.QLabel(self.dockWidgetContents_3)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_9.addWidget(self.label_8)
        self.dsbxThresholdSpec = QtGui.QDoubleSpinBox(self.dockWidgetContents_3)
        self.dsbxThresholdSpec.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dsbxThresholdSpec.sizePolicy().hasHeightForWidth())
        self.dsbxThresholdSpec.setSizePolicy(sizePolicy)
        self.dsbxThresholdSpec.setWrapping(False)
        self.dsbxThresholdSpec.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.dsbxThresholdSpec.setMinimum(1.0)
        self.dsbxThresholdSpec.setSingleStep(5.0)
        self.dsbxThresholdSpec.setProperty("value", 95.0)
        self.dsbxThresholdSpec.setObjectName(_fromUtf8("dsbxThresholdSpec"))
        self.horizontalLayout_9.addWidget(self.dsbxThresholdSpec)
        self.horizontalLayout_9.setStretch(1, 1)
        self.gridLayout_3.addLayout(self.horizontalLayout_9, 0, 1, 1, 1)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_7 = QtGui.QLabel(self.dockWidgetContents_3)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_8.addWidget(self.label_7)
        self.dsbxminSizeTime = QtGui.QDoubleSpinBox(self.dockWidgetContents_3)
        self.dsbxminSizeTime.setEnabled(True)
        self.dsbxminSizeTime.setObjectName(_fromUtf8("dsbxminSizeTime"))
        self.horizontalLayout_8.addWidget(self.dsbxminSizeTime)
        self.dsbxMinSizeFreq = QtGui.QDoubleSpinBox(self.dockWidgetContents_3)
        self.dsbxMinSizeFreq.setEnabled(True)
        self.dsbxMinSizeFreq.setObjectName(_fromUtf8("dsbxMinSizeFreq"))
        self.horizontalLayout_8.addWidget(self.dsbxMinSizeFreq)
        self.horizontalLayout_8.setStretch(1, 1)
        self.horizontalLayout_8.setStretch(2, 1)
        self.gridLayout_3.addLayout(self.horizontalLayout_8, 1, 1, 1, 1)
        self.dockWidgetEspgram.setWidget(self.dockWidgetContents_3)
        self.gridLayout_2.addWidget(self.dockWidgetEspgram, 1, 0, 1, 1)
        self.dockWidgetParametrers = QtGui.QDockWidget(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetParametrers.sizePolicy().hasHeightForWidth())
        self.dockWidgetParametrers.setSizePolicy(sizePolicy)
        self.dockWidgetParametrers.setFloating(False)
        self.dockWidgetParametrers.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.dockWidgetParametrers.setObjectName(_fromUtf8("dockWidgetParametrers"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout_4 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gboxSpectral = QtGui.QGroupBox(self.dockWidgetContents)
        self.gboxSpectral.setObjectName(_fromUtf8("gboxSpectral"))
        self.formLayout_9 = QtGui.QFormLayout(self.gboxSpectral)
        self.formLayout_9.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_9.setObjectName(_fromUtf8("formLayout_9"))
        self.cbxPeakFreq = QtGui.QCheckBox(self.gboxSpectral)
        self.cbxPeakFreq.setChecked(True)
        self.cbxPeakFreq.setObjectName(_fromUtf8("cbxPeakFreq"))
        self.formLayout_9.setWidget(1, QtGui.QFormLayout.LabelRole, self.cbxPeakFreq)
        self.cbxMaxFreq = QtGui.QCheckBox(self.gboxSpectral)
        self.cbxMaxFreq.setChecked(True)
        self.cbxMaxFreq.setObjectName(_fromUtf8("cbxMaxFreq"))
        self.formLayout_9.setWidget(2, QtGui.QFormLayout.LabelRole, self.cbxMaxFreq)
        self.cbxMinFreq = QtGui.QCheckBox(self.gboxSpectral)
        self.cbxMinFreq.setChecked(True)
        self.cbxMinFreq.setObjectName(_fromUtf8("cbxMinFreq"))
        self.formLayout_9.setWidget(3, QtGui.QFormLayout.LabelRole, self.cbxMinFreq)
        self.gridLayout_4.addWidget(self.gboxSpectral, 1, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout_10 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_10.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_10.setObjectName(_fromUtf8("formLayout_10"))
        self.cbxmeasurementLocationStart = QtGui.QCheckBox(self.groupBox)
        self.cbxmeasurementLocationStart.setChecked(True)
        self.cbxmeasurementLocationStart.setObjectName(_fromUtf8("cbxmeasurementLocationStart"))
        self.formLayout_10.setWidget(0, QtGui.QFormLayout.LabelRole, self.cbxmeasurementLocationStart)
        self.cbxmeasurementLocationCenter = QtGui.QCheckBox(self.groupBox)
        self.cbxmeasurementLocationCenter.setChecked(True)
        self.cbxmeasurementLocationCenter.setObjectName(_fromUtf8("cbxmeasurementLocationCenter"))
        self.formLayout_10.setWidget(2, QtGui.QFormLayout.LabelRole, self.cbxmeasurementLocationCenter)
        self.cbxmeasurementLocationEnd = QtGui.QCheckBox(self.groupBox)
        self.cbxmeasurementLocationEnd.setChecked(True)
        self.cbxmeasurementLocationEnd.setObjectName(_fromUtf8("cbxmeasurementLocationEnd"))
        self.formLayout_10.setWidget(4, QtGui.QFormLayout.LabelRole, self.cbxmeasurementLocationEnd)
        self.cbxmeasurementLocationQuartile25 = QtGui.QCheckBox(self.groupBox)
        self.cbxmeasurementLocationQuartile25.setChecked(True)
        self.cbxmeasurementLocationQuartile25.setObjectName(_fromUtf8("cbxmeasurementLocationQuartile25"))
        self.formLayout_10.setWidget(1, QtGui.QFormLayout.LabelRole, self.cbxmeasurementLocationQuartile25)
        self.cbxmeasurementLocationQuartile75 = QtGui.QCheckBox(self.groupBox)
        self.cbxmeasurementLocationQuartile75.setChecked(True)
        self.cbxmeasurementLocationQuartile75.setObjectName(_fromUtf8("cbxmeasurementLocationQuartile75"))
        self.formLayout_10.setWidget(3, QtGui.QFormLayout.LabelRole, self.cbxmeasurementLocationQuartile75)
        self.gridLayout_4.addWidget(self.groupBox, 1, 1, 1, 1)
        self.gboxOscilogramParameters = QtGui.QGroupBox(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gboxOscilogramParameters.sizePolicy().hasHeightForWidth())
        self.gboxOscilogramParameters.setSizePolicy(sizePolicy)
        self.gboxOscilogramParameters.setObjectName(_fromUtf8("gboxOscilogramParameters"))
        self.formLayout_4 = QtGui.QFormLayout(self.gboxOscilogramParameters)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.cbxDuration = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxDuration.setChecked(True)
        self.cbxDuration.setObjectName(_fromUtf8("cbxDuration"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.cbxDuration)
        self.cbxPeekToPeek = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxPeekToPeek.setChecked(True)
        self.cbxPeekToPeek.setObjectName(_fromUtf8("cbxPeekToPeek"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.cbxPeekToPeek)
        self.cbxStartTime = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxStartTime.setChecked(True)
        self.cbxStartTime.setObjectName(_fromUtf8("cbxStartTime"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.cbxStartTime)
        self.cbxEndTime = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxEndTime.setChecked(True)
        self.cbxEndTime.setObjectName(_fromUtf8("cbxEndTime"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.cbxEndTime)
        self.cbxStartToMax = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxStartToMax.setChecked(True)
        self.cbxStartToMax.setObjectName(_fromUtf8("cbxStartToMax"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.LabelRole, self.cbxStartToMax)
        self.cbxRms = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxRms.setChecked(True)
        self.cbxRms.setObjectName(_fromUtf8("cbxRms"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.cbxRms)
        self.gridLayout_4.addWidget(self.gboxOscilogramParameters, 0, 0, 1, 2)
        self.dockWidgetParametrers.setWidget(self.dockWidgetContents)
        self.gridLayout_2.addWidget(self.dockWidgetParametrers, 3, 0, 1, 1)
        self.dockWidgetOscilogram = QtGui.QDockWidget(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetOscilogram.sizePolicy().hasHeightForWidth())
        self.dockWidgetOscilogram.setSizePolicy(sizePolicy)
        self.dockWidgetOscilogram.setFloating(False)
        self.dockWidgetOscilogram.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.dockWidgetOscilogram.setObjectName(_fromUtf8("dockWidgetOscilogram"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_6 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_7.addWidget(self.label_6)
        self.dsbxThreshold = QtGui.QDoubleSpinBox(self.dockWidgetContents_2)
        self.dsbxThreshold.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.dsbxThreshold.setMinimum(-60.0)
        self.dsbxThreshold.setMaximum(0.0)
        self.dsbxThreshold.setObjectName(_fromUtf8("dsbxThreshold"))
        self.horizontalLayout_7.addWidget(self.dsbxThreshold)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setSpacing(6)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.label_10 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_11.addWidget(self.label_10)
        self.dsbxThreshold2 = QtGui.QDoubleSpinBox(self.dockWidgetContents_2)
        self.dsbxThreshold2.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.dsbxThreshold2.setMinimum(-60.0)
        self.dsbxThreshold2.setMaximum(0.0)
        self.dsbxThreshold2.setProperty("value", 0.0)
        self.dsbxThreshold2.setObjectName(_fromUtf8("dsbxThreshold2"))
        self.horizontalLayout_11.addWidget(self.dsbxThreshold2)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_11)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_4 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        self.dsbxDecay = QtGui.QDoubleSpinBox(self.dockWidgetContents_2)
        self.dsbxDecay.setObjectName(_fromUtf8("dsbxDecay"))
        self.horizontalLayout_5.addWidget(self.dsbxDecay)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.dsbxMinSize = QtGui.QDoubleSpinBox(self.dockWidgetContents_2)
        self.dsbxMinSize.setObjectName(_fromUtf8("dsbxMinSize"))
        self.horizontalLayout_3.addWidget(self.dsbxMinSize)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_5 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_6.addWidget(self.label_5)
        self.sbxSoftFactor = QtGui.QSpinBox(self.dockWidgetContents_2)
        self.sbxSoftFactor.setMinimum(2)
        self.sbxSoftFactor.setMaximum(10)
        self.sbxSoftFactor.setSingleStep(2)
        self.sbxSoftFactor.setProperty("value", 6)
        self.sbxSoftFactor.setObjectName(_fromUtf8("sbxSoftFactor"))
        self.horizontalLayout_6.addWidget(self.sbxSoftFactor)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.dsbxMergeFactor = QtGui.QDoubleSpinBox(self.dockWidgetContents_2)
        self.dsbxMergeFactor.setObjectName(_fromUtf8("dsbxMergeFactor"))
        self.horizontalLayout_4.addWidget(self.dsbxMergeFactor)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.dockWidgetOscilogram.setWidget(self.dockWidgetContents_2)
        self.gridLayout_2.addWidget(self.dockWidgetOscilogram, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.groupBox_2)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.widget = QSignalVisualizerWidget(Dialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Detection Settings", None))
        self.dockWidgetEspgram.setWindowTitle(_translate("Dialog", "Espectrogram", None))
        self.label_8.setText(_translate("Dialog", "Threshold:", None))
        self.dsbxThresholdSpec.setSuffix(_translate("Dialog", "%", None))
        self.label_7.setText(_translate("Dialog", "Minimum size:", None))
        self.dsbxminSizeTime.setSuffix(_translate("Dialog", " ms", None))
        self.dsbxMinSizeFreq.setSuffix(_translate("Dialog", " kHz", None))
        self.dockWidgetParametrers.setWindowTitle(_translate("Dialog", "Parameters", None))
        self.gboxSpectral.setTitle(_translate("Dialog", "Spectral Parameters", None))
        self.cbxPeakFreq.setText(_translate("Dialog", "Peak Frecuency", None))
        self.cbxMaxFreq.setText(_translate("Dialog", "Max Frecuency", None))
        self.cbxMinFreq.setText(_translate("Dialog", "Min Frecuency", None))
        self.groupBox.setTitle(_translate("Dialog", "Measurement Location", None))
        self.cbxmeasurementLocationStart.setText(_translate("Dialog", "Start", None))
        self.cbxmeasurementLocationCenter.setText(_translate("Dialog", "Center", None))
        self.cbxmeasurementLocationEnd.setText(_translate("Dialog", "End", None))
        self.cbxmeasurementLocationQuartile25.setText(_translate("Dialog", "Quartile25", None))
        self.cbxmeasurementLocationQuartile75.setText(_translate("Dialog", "Quartile75", None))
        self.gboxOscilogramParameters.setTitle(_translate("Dialog", "Temporal Parameters", None))
        self.cbxDuration.setText(_translate("Dialog", "Duration", None))
        self.cbxPeekToPeek.setText(_translate("Dialog", "Peek to Peek", None))
        self.cbxStartTime.setText(_translate("Dialog", "Start Time", None))
        self.cbxEndTime.setText(_translate("Dialog", "End Time", None))
        self.cbxStartToMax.setText(_translate("Dialog", "Start To Max", None))
        self.cbxRms.setText(_translate("Dialog", "RMS", None))
        self.dockWidgetOscilogram.setWindowTitle(_translate("Dialog", "Oscilogram ", None))
        self.label_6.setText(_translate("Dialog", "Threshold:", None))
        self.dsbxThreshold.setSuffix(_translate("Dialog", "dB", None))
        self.label_10.setText(_translate("Dialog", "Threshold 2:", None))
        self.dsbxThreshold2.setSuffix(_translate("Dialog", "dB", None))
        self.label_4.setText(_translate("Dialog", "Decay:", None))
        self.dsbxDecay.setSuffix(_translate("Dialog", " ms", None))
        self.label_2.setText(_translate("Dialog", "Minimum size:", None))
        self.dsbxMinSize.setSuffix(_translate("Dialog", " ms", None))
        self.label_5.setText(_translate("Dialog", "Soft factor:", None))
        self.label_3.setText(_translate("Dialog", "Merge factor:", None))
        self.dsbxMergeFactor.setSuffix(_translate("Dialog", " ms", None))
        self.widget.setToolTip(_translate("Dialog", "<html><head/><body><p>Signal to learn about algorithm parameters</p></body></html>", None))

from Graphic_Interface.Widgets.QSignalVisualizerWidget import QSignalVisualizerWidget
