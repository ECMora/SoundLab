# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Biologia\SISTEMA\DuettoSystem\Graphic_Interface\UI Files\ui_elemDetectSettings.ui'
#
# Created: Tue May 06 12:33:07 2014
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
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(1100, 664)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(1100, 660))
        Dialog.setMaximumSize(QtCore.QSize(1100, 664))
        Dialog.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:pad, x1:0.006, y1:0.017, x2:0.886, y2:0.892045, stop:0.0340909 rgba(94, 116, 236, 255), stop:1 rgba(255, 255, 255, 255));\n"
"font: 75 10pt \"MS Shell Dlg 2\";"))
        Dialog.setModal(False)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget = QSignalVisualizerWidget(Dialog)
        self.widget.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout_5 = QtGui.QFormLayout(self.widget)
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.horizontalLayout.addWidget(self.widget)
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout_6 = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout_6.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.gboxSpectral = QtGui.QGroupBox(self.groupBox_3)
        self.gboxSpectral.setObjectName(_fromUtf8("gboxSpectral"))
        self.gridLayout_4 = QtGui.QGridLayout(self.gboxSpectral)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.cbxPeaksAbove = QtGui.QCheckBox(self.gboxSpectral)
        self.cbxPeaksAbove.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxPeaksAbove.setChecked(False)
        self.cbxPeaksAbove.setObjectName(_fromUtf8("cbxPeaksAbove"))
        self.gridLayout_4.addWidget(self.cbxPeaksAbove, 7, 0, 1, 1)
        self.cbxMinFreq = QtGui.QCheckBox(self.gboxSpectral)
        self.cbxMinFreq.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxMinFreq.setChecked(False)
        self.cbxMinFreq.setObjectName(_fromUtf8("cbxMinFreq"))
        self.gridLayout_4.addWidget(self.cbxMinFreq, 5, 0, 1, 1)
        self.cbxPeakFreq = QtGui.QCheckBox(self.gboxSpectral)
        self.cbxPeakFreq.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxPeakFreq.setChecked(False)
        self.cbxPeakFreq.setObjectName(_fromUtf8("cbxPeakFreq"))
        self.gridLayout_4.addWidget(self.cbxPeakFreq, 2, 0, 1, 1)
        self.spbxSpectralLocMeasureThreshold = QtGui.QSpinBox(self.gboxSpectral)
        self.spbxSpectralLocMeasureThreshold.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.spbxSpectralLocMeasureThreshold.setMinimum(-100)
        self.spbxSpectralLocMeasureThreshold.setMaximum(0)
        self.spbxSpectralLocMeasureThreshold.setProperty("value", -20)
        self.spbxSpectralLocMeasureThreshold.setObjectName(_fromUtf8("spbxSpectralLocMeasureThreshold"))
        self.gridLayout_4.addWidget(self.spbxSpectralLocMeasureThreshold, 4, 1, 1, 1)
        self.cbxBandWidth = QtGui.QCheckBox(self.gboxSpectral)
        self.cbxBandWidth.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxBandWidth.setChecked(False)
        self.cbxBandWidth.setObjectName(_fromUtf8("cbxBandWidth"))
        self.gridLayout_4.addWidget(self.cbxBandWidth, 6, 0, 1, 1)
        self.spbxPeaksThreshold = QtGui.QSpinBox(self.gboxSpectral)
        self.spbxPeaksThreshold.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.spbxPeaksThreshold.setMinimum(-90)
        self.spbxPeaksThreshold.setMaximum(0)
        self.spbxPeaksThreshold.setProperty("value", -20)
        self.spbxPeaksThreshold.setObjectName(_fromUtf8("spbxPeaksThreshold"))
        self.gridLayout_4.addWidget(self.spbxPeaksThreshold, 7, 1, 1, 1)
        self.cbxSpectralElems = QtGui.QCheckBox(self.gboxSpectral)
        self.cbxSpectralElems.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxSpectralElems.setChecked(False)
        self.cbxSpectralElems.setObjectName(_fromUtf8("cbxSpectralElems"))
        self.gridLayout_4.addWidget(self.cbxSpectralElems, 1, 0, 1, 1)
        self.cbxPeakAmplitude = QtGui.QCheckBox(self.gboxSpectral)
        self.cbxPeakAmplitude.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxPeakAmplitude.setChecked(False)
        self.cbxPeakAmplitude.setObjectName(_fromUtf8("cbxPeakAmplitude"))
        self.gridLayout_4.addWidget(self.cbxPeakAmplitude, 3, 0, 1, 1)
        self.cbxMaxFreq = QtGui.QCheckBox(self.gboxSpectral)
        self.cbxMaxFreq.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxMaxFreq.setChecked(False)
        self.cbxMaxFreq.setObjectName(_fromUtf8("cbxMaxFreq"))
        self.gridLayout_4.addWidget(self.cbxMaxFreq, 4, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 0, 0, 1, 1)
        self.formLayout_6.setWidget(3, QtGui.QFormLayout.LabelRole, self.gboxSpectral)
        self.groupBox_5 = QtGui.QGroupBox(self.groupBox_3)
        self.groupBox_5.setEnabled(False)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_8 = QtGui.QLabel(self.groupBox_5)
        self.label_8.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_9.addWidget(self.label_8)
        self.dsbxThresholdSpec = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.dsbxThresholdSpec.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dsbxThresholdSpec.sizePolicy().hasHeightForWidth())
        self.dsbxThresholdSpec.setSizePolicy(sizePolicy)
        self.dsbxThresholdSpec.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.dsbxThresholdSpec.setWrapping(False)
        self.dsbxThresholdSpec.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.dsbxThresholdSpec.setMinimum(1.0)
        self.dsbxThresholdSpec.setSingleStep(5.0)
        self.dsbxThresholdSpec.setProperty("value", 95.0)
        self.dsbxThresholdSpec.setObjectName(_fromUtf8("dsbxThresholdSpec"))
        self.horizontalLayout_9.addWidget(self.dsbxThresholdSpec)
        self.horizontalLayout_9.setStretch(1, 1)
        self.gridLayout.addLayout(self.horizontalLayout_9, 2, 0, 1, 1)
        self.cbxSpectralSubelements = QtGui.QCheckBox(self.groupBox_5)
        self.cbxSpectralSubelements.setEnabled(False)
        self.cbxSpectralSubelements.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxSpectralSubelements.setChecked(False)
        self.cbxSpectralSubelements.setObjectName(_fromUtf8("cbxSpectralSubelements"))
        self.gridLayout.addWidget(self.cbxSpectralSubelements, 1, 0, 1, 1)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_7 = QtGui.QLabel(self.groupBox_5)
        self.label_7.setEnabled(False)
        self.label_7.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_8.addWidget(self.label_7)
        self.dsbxminSizeTime = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.dsbxminSizeTime.setEnabled(False)
        self.dsbxminSizeTime.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.dsbxminSizeTime.setObjectName(_fromUtf8("dsbxminSizeTime"))
        self.horizontalLayout_8.addWidget(self.dsbxminSizeTime)
        self.dsbxMinSizeFreq = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.dsbxMinSizeFreq.setEnabled(False)
        self.dsbxMinSizeFreq.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.dsbxMinSizeFreq.setObjectName(_fromUtf8("dsbxMinSizeFreq"))
        self.horizontalLayout_8.addWidget(self.dsbxMinSizeFreq)
        self.horizontalLayout_8.setStretch(1, 1)
        self.horizontalLayout_8.setStretch(2, 1)
        self.gridLayout.addLayout(self.horizontalLayout_8, 3, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.SpanningRole, self.groupBox_5)
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox_3)
        self.groupBox_4.setFlat(False)
        self.groupBox_4.setCheckable(False)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.formLayout_7 = QtGui.QFormLayout(self.groupBox_4)
        self.formLayout_7.setObjectName(_fromUtf8("formLayout_7"))
        self.label = QtGui.QLabel(self.groupBox_4)
        self.label.setStyleSheet(_fromUtf8("background-color: rgb(108, 168, 214);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_7.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.cmbxDetectionMethod = QtGui.QComboBox(self.groupBox_4)
        self.cmbxDetectionMethod.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.cmbxDetectionMethod.setObjectName(_fromUtf8("cmbxDetectionMethod"))
        self.cmbxDetectionMethod.addItem(_fromUtf8(""))
        self.cmbxDetectionMethod.addItem(_fromUtf8(""))
        self.cmbxDetectionMethod.addItem(_fromUtf8(""))
        self.cmbxDetectionMethod.addItem(_fromUtf8(""))
        self.cmbxDetectionMethod.addItem(_fromUtf8(""))
        self.cmbxDetectionMethod.addItem(_fromUtf8(""))
        self.cmbxDetectionMethod.addItem(_fromUtf8(""))
        self.cmbxDetectionMethod.addItem(_fromUtf8(""))
        self.cmbxDetectionMethod.addItem(_fromUtf8(""))
        self.formLayout_7.setWidget(1, QtGui.QFormLayout.FieldRole, self.cmbxDetectionMethod)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_6 = QtGui.QLabel(self.groupBox_4)
        self.label_6.setEnabled(True)
        self.label_6.setStyleSheet(_fromUtf8("background-color: rgb(108, 168, 214);"))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_7.addWidget(self.label_6)
        self.dsbxThreshold = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.dsbxThreshold.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.dsbxThreshold.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.dsbxThreshold.setMinimum(-60.0)
        self.dsbxThreshold.setMaximum(0.0)
        self.dsbxThreshold.setObjectName(_fromUtf8("dsbxThreshold"))
        self.horizontalLayout_7.addWidget(self.dsbxThreshold)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setSpacing(6)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.checboxAutomaticThreshold = QtGui.QCheckBox(self.groupBox_4)
        self.checboxAutomaticThreshold.setChecked(True)
        self.checboxAutomaticThreshold.setObjectName(_fromUtf8("checboxAutomaticThreshold"))
        self.horizontalLayout_11.addWidget(self.checboxAutomaticThreshold)
        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setStyleSheet(_fromUtf8("background-color: rgb(108, 168, 214);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_11.addWidget(self.label_2)
        self.dsbxMinSize = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.dsbxMinSize.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.dsbxMinSize.setMinimum(0.01)
        self.dsbxMinSize.setProperty("value", 1.0)
        self.dsbxMinSize.setObjectName(_fromUtf8("dsbxMinSize"))
        self.horizontalLayout_11.addWidget(self.dsbxMinSize)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_11)
        self.formLayout_7.setLayout(2, QtGui.QFormLayout.SpanningRole, self.horizontalLayout_7)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setStyleSheet(_fromUtf8("background-color: rgb(108, 168, 214);"))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        self.dsbxDecay = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.dsbxDecay.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.dsbxDecay.setMinimum(0.1)
        self.dsbxDecay.setMaximum(200.0)
        self.dsbxDecay.setProperty("value", 1.0)
        self.dsbxDecay.setObjectName(_fromUtf8("dsbxDecay"))
        self.horizontalLayout_5.addWidget(self.dsbxDecay)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_10 = QtGui.QLabel(self.groupBox_4)
        self.label_10.setStyleSheet(_fromUtf8("background-color: rgb(108, 168, 214);"))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_3.addWidget(self.label_10)
        self.dsbxThreshold2 = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.dsbxThreshold2.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.dsbxThreshold2.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.dsbxThreshold2.setMinimum(-60.0)
        self.dsbxThreshold2.setMaximum(0.0)
        self.dsbxThreshold2.setProperty("value", 0.0)
        self.dsbxThreshold2.setObjectName(_fromUtf8("dsbxThreshold2"))
        self.horizontalLayout_3.addWidget(self.dsbxThreshold2)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.formLayout_7.setLayout(3, QtGui.QFormLayout.SpanningRole, self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setStyleSheet(_fromUtf8("background-color: rgb(108, 168, 214);"))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_6.addWidget(self.label_5)
        self.sbxSoftFactor = QtGui.QSpinBox(self.groupBox_4)
        self.sbxSoftFactor.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.sbxSoftFactor.setMinimum(2)
        self.sbxSoftFactor.setMaximum(10)
        self.sbxSoftFactor.setSingleStep(2)
        self.sbxSoftFactor.setProperty("value", 6)
        self.sbxSoftFactor.setObjectName(_fromUtf8("sbxSoftFactor"))
        self.horizontalLayout_6.addWidget(self.sbxSoftFactor)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setStyleSheet(_fromUtf8("background-color: rgb(108, 168, 214);"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.dsbxMergeFactor = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.dsbxMergeFactor.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.dsbxMergeFactor.setDecimals(0)
        self.dsbxMergeFactor.setMaximum(49.0)
        self.dsbxMergeFactor.setSingleStep(1.0)
        self.dsbxMergeFactor.setProperty("value", 5.0)
        self.dsbxMergeFactor.setObjectName(_fromUtf8("dsbxMergeFactor"))
        self.horizontalLayout_4.addWidget(self.dsbxMergeFactor)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.formLayout_7.setLayout(4, QtGui.QFormLayout.SpanningRole, self.horizontalLayout_6)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout_7.setItem(0, QtGui.QFormLayout.LabelRole, spacerItem2)
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.SpanningRole, self.groupBox_4)
        self.groupBox = QtGui.QGroupBox(self.groupBox_3)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.cbxmeasurementLocationStart = QtGui.QCheckBox(self.groupBox)
        self.cbxmeasurementLocationStart.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxmeasurementLocationStart.setChecked(False)
        self.cbxmeasurementLocationStart.setObjectName(_fromUtf8("cbxmeasurementLocationStart"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.cbxmeasurementLocationStart)
        self.cbxmeasurementLocationCenter = QtGui.QCheckBox(self.groupBox)
        self.cbxmeasurementLocationCenter.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxmeasurementLocationCenter.setChecked(False)
        self.cbxmeasurementLocationCenter.setObjectName(_fromUtf8("cbxmeasurementLocationCenter"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.cbxmeasurementLocationCenter)
        self.cbxmeasurementLocationEnd = QtGui.QCheckBox(self.groupBox)
        self.cbxmeasurementLocationEnd.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxmeasurementLocationEnd.setChecked(False)
        self.cbxmeasurementLocationEnd.setObjectName(_fromUtf8("cbxmeasurementLocationEnd"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.cbxmeasurementLocationEnd)
        self.cbxmeasurementLocationQuartile25 = QtGui.QCheckBox(self.groupBox)
        self.cbxmeasurementLocationQuartile25.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxmeasurementLocationQuartile25.setChecked(False)
        self.cbxmeasurementLocationQuartile25.setObjectName(_fromUtf8("cbxmeasurementLocationQuartile25"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cbxmeasurementLocationQuartile25)
        self.cbxmeasurementLocationAverage = QtGui.QCheckBox(self.groupBox)
        self.cbxmeasurementLocationAverage.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.cbxmeasurementLocationAverage.setObjectName(_fromUtf8("cbxmeasurementLocationAverage"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.cbxmeasurementLocationAverage)
        self.cbxmeasurementLocationQuartile75 = QtGui.QCheckBox(self.groupBox)
        self.cbxmeasurementLocationQuartile75.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxmeasurementLocationQuartile75.setChecked(False)
        self.cbxmeasurementLocationQuartile75.setObjectName(_fromUtf8("cbxmeasurementLocationQuartile75"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cbxmeasurementLocationQuartile75)
        spacerItem3 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(0, QtGui.QFormLayout.LabelRole, spacerItem3)
        self.formLayout_6.setWidget(3, QtGui.QFormLayout.FieldRole, self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(self.groupBox_3)
        self.buttonBox.setStyleSheet(_fromUtf8("font: 75 11pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(8, 100, 180);\n"
"color: rgb(255, 255, 255);"))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout_6.setWidget(6, QtGui.QFormLayout.FieldRole, self.buttonBox)
        self.gboxOscilogramParameters = QtGui.QGroupBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gboxOscilogramParameters.sizePolicy().hasHeightForWidth())
        self.gboxOscilogramParameters.setSizePolicy(sizePolicy)
        self.gboxOscilogramParameters.setObjectName(_fromUtf8("gboxOscilogramParameters"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gboxOscilogramParameters)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.cbxPeekToPeek = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxPeekToPeek.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxPeekToPeek.setChecked(False)
        self.cbxPeekToPeek.setObjectName(_fromUtf8("cbxPeekToPeek"))
        self.gridLayout_2.addWidget(self.cbxPeekToPeek, 1, 3, 1, 1)
        self.cbxRms = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxRms.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxRms.setChecked(False)
        self.cbxRms.setObjectName(_fromUtf8("cbxRms"))
        self.gridLayout_2.addWidget(self.cbxRms, 4, 2, 1, 1)
        self.cbxDuration = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxDuration.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxDuration.setChecked(False)
        self.cbxDuration.setObjectName(_fromUtf8("cbxDuration"))
        self.gridLayout_2.addWidget(self.cbxDuration, 1, 2, 1, 1)
        self.cbxEndTime = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxEndTime.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxEndTime.setChecked(False)
        self.cbxEndTime.setObjectName(_fromUtf8("cbxEndTime"))
        self.gridLayout_2.addWidget(self.cbxEndTime, 4, 1, 1, 1)
        self.cbxStartTime = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxStartTime.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxStartTime.setChecked(False)
        self.cbxStartTime.setObjectName(_fromUtf8("cbxStartTime"))
        self.gridLayout_2.addWidget(self.cbxStartTime, 1, 1, 1, 1)
        self.cbxStartToMax = QtGui.QCheckBox(self.gboxOscilogramParameters)
        self.cbxStartToMax.setStyleSheet(_fromUtf8("background-color: rgb(244, 244, 244);"))
        self.cbxStartToMax.setChecked(False)
        self.cbxStartToMax.setObjectName(_fromUtf8("cbxStartToMax"))
        self.gridLayout_2.addWidget(self.cbxStartToMax, 4, 3, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem4, 0, 1, 1, 1)
        self.formLayout_6.setWidget(2, QtGui.QFormLayout.SpanningRole, self.gboxOscilogramParameters)
        self.horizontalLayout.addWidget(self.groupBox_3)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Detection Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.widget.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Signal to learn about algorithm parameters</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.gboxSpectral.setTitle(QtGui.QApplication.translate("Dialog", "Spectral Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxPeaksAbove.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>The amount of peaks above threshold in the spectral location of measurement</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxPeaksAbove.setText(QtGui.QApplication.translate("Dialog", "Peaks Above", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxMinFreq.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>The max frecuency above the threshold in the spectral location of measurement</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxMinFreq.setText(QtGui.QApplication.translate("Dialog", "Min Frecuency", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxPeakFreq.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>The peak frecuency of the measurement location</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxPeakFreq.setText(QtGui.QApplication.translate("Dialog", "Peak Frecuency", None, QtGui.QApplication.UnicodeUTF8))
        self.spbxSpectralLocMeasureThreshold.setSuffix(QtGui.QApplication.translate("Dialog", "dB", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxBandWidth.setText(QtGui.QApplication.translate("Dialog", "Band Width", None, QtGui.QApplication.UnicodeUTF8))
        self.spbxPeaksThreshold.setSuffix(QtGui.QApplication.translate("Dialog", "dB", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxSpectralElems.setText(QtGui.QApplication.translate("Dialog", "Spectral Elems", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxPeakAmplitude.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>The amplitude of spectrum in the peak frecuency.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxPeakAmplitude.setText(QtGui.QApplication.translate("Dialog", "Peak Amplitude", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxMaxFreq.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>The min frecuency above threshold in the spectral location of measurement</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxMaxFreq.setText(QtGui.QApplication.translate("Dialog", "Max Frecuency", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("Dialog", "Spectral Detection Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>The percentile threshold to detect subelements in spectrogram. Regions above this value are detected</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "Threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.dsbxThresholdSpec.setSuffix(QtGui.QApplication.translate("Dialog", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxSpectralSubelements.setText(QtGui.QApplication.translate("Dialog", "Detect Spectral Subelements", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Minimum size of spectral subelements in ms and Khz</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Minimum size:", None, QtGui.QApplication.UnicodeUTF8))
        self.dsbxminSizeTime.setSuffix(QtGui.QApplication.translate("Dialog", " ms", None, QtGui.QApplication.UnicodeUTF8))
        self.dsbxMinSizeFreq.setSuffix(QtGui.QApplication.translate("Dialog", " kHz", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("Dialog", "Temporal Detection Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", " Detection Method ", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbxDetectionMethod.setItemText(0, QtGui.QApplication.translate("Dialog", "Local Max", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbxDetectionMethod.setItemText(1, QtGui.QApplication.translate("Dialog", "Local Hold Time", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbxDetectionMethod.setItemText(2, QtGui.QApplication.translate("Dialog", "Local Max Proportion", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbxDetectionMethod.setItemText(3, QtGui.QApplication.translate("Dialog", "Interval RMS", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbxDetectionMethod.setItemText(4, QtGui.QApplication.translate("Dialog", "Interval Max Media", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbxDetectionMethod.setItemText(5, QtGui.QApplication.translate("Dialog", "Interval Max Proportion", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbxDetectionMethod.setItemText(6, QtGui.QApplication.translate("Dialog", "Intervals Frecuencies", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbxDetectionMethod.setItemText(7, QtGui.QApplication.translate("Dialog", "Decay Envelope ", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbxDetectionMethod.setItemText(8, QtGui.QApplication.translate("Dialog", "Rms Envelope", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>The elements above detection threshold</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.dsbxThreshold.setSuffix(QtGui.QApplication.translate("Dialog", "dB", None, QtGui.QApplication.UnicodeUTF8))
        self.checboxAutomaticThreshold.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Automatic Threshold selection</p><p><br/></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checboxAutomaticThreshold.setText(QtGui.QApplication.translate("Dialog", "Auto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Element minimum size </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Min size:", None, QtGui.QApplication.UnicodeUTF8))
        self.dsbxMinSize.setSuffix(QtGui.QApplication.translate("Dialog", " ms", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Jump to prevent locals falls of signal. Noiser signal bigger decay</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Decay:", None, QtGui.QApplication.UnicodeUTF8))
        self.dsbxDecay.setSuffix(QtGui.QApplication.translate("Dialog", " ms", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>The elements above second trheshold and with a piece above detection threshold</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "Threshold 2:", None, QtGui.QApplication.UnicodeUTF8))
        self.dsbxThreshold2.setSuffix(QtGui.QApplication.translate("Dialog", "dB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Soft factor:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Merge elements closer than this factor</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Merge factor:", None, QtGui.QApplication.UnicodeUTF8))
        self.dsbxMergeFactor.setSuffix(QtGui.QApplication.translate("Dialog", " %", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Measurement Location", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxmeasurementLocationStart.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p> Spectral parameters location of measurement. </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxmeasurementLocationStart.setText(QtGui.QApplication.translate("Dialog", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxmeasurementLocationCenter.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p> Spectral parameters location of measurement. </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxmeasurementLocationCenter.setText(QtGui.QApplication.translate("Dialog", "Center", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxmeasurementLocationEnd.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p> Spectral parameters location of measurement. </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxmeasurementLocationEnd.setText(QtGui.QApplication.translate("Dialog", "End", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxmeasurementLocationQuartile25.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p> Spectral parameters location of measurement. </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxmeasurementLocationQuartile25.setText(QtGui.QApplication.translate("Dialog", "Quartile25", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxmeasurementLocationAverage.setText(QtGui.QApplication.translate("Dialog", "Mean", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxmeasurementLocationQuartile75.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p> Spectral parameters location of measurement. </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxmeasurementLocationQuartile75.setText(QtGui.QApplication.translate("Dialog", "Quartile75", None, QtGui.QApplication.UnicodeUTF8))
        self.gboxOscilogramParameters.setTitle(QtGui.QApplication.translate("Dialog", "Temporal Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxPeekToPeek.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>peek to peek value of the element</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxPeekToPeek.setText(QtGui.QApplication.translate("Dialog", "Peek to Peek", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxRms.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>rms of the element</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxRms.setText(QtGui.QApplication.translate("Dialog", "RMS", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxDuration.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Duration time of element</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxDuration.setText(QtGui.QApplication.translate("Dialog", "Duration", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxEndTime.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>End time of element</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxEndTime.setText(QtGui.QApplication.translate("Dialog", "End Time", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxStartTime.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Start time of element</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxStartTime.setText(QtGui.QApplication.translate("Dialog", "Start Time", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxStartToMax.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Distance from the element start to its max value</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxStartToMax.setText(QtGui.QApplication.translate("Dialog", "Start To Max", None, QtGui.QApplication.UnicodeUTF8))

from Graphic_Interface.Widgets.QSignalVisualizerWidget import QSignalVisualizerWidget
