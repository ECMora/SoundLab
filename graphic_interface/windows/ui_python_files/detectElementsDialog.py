# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Fac Biologia\DUETTO PROGRAMS\Desktop\Sound Lab\duetto-SoundLab\graphic_interface\UI_Files\detectElementsDialog.ui'
#
# Created: Wed Jul 01 16:38:39 2015
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
        Dialog.resize(766, 466)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(1100, 664))
        Dialog.setStyleSheet(_fromUtf8(""))
        Dialog.setModal(False)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget_2 = QtGui.QWidget(Dialog)
        self.widget_2.setStyleSheet(_fromUtf8(""))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.buttonBox = QtGui.QDialogButtonBox(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setMaximumSize(QtCore.QSize(250, 16777215))
        self.buttonBox.setStyleSheet(_fromUtf8(""))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 2, 1, 1)
        self.dock_segm_classif = QtGui.QDockWidget(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_segm_classif.sizePolicy().hasHeightForWidth())
        self.dock_segm_classif.setSizePolicy(sizePolicy)
        self.dock_segm_classif.setMinimumSize(QtCore.QSize(300, 84))
        self.dock_segm_classif.setMaximumSize(QtCore.QSize(524287, 524287))
        self.dock_segm_classif.setStyleSheet(_fromUtf8(""))
        self.dock_segm_classif.setFloating(False)
        self.dock_segm_classif.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        self.dock_segm_classif.setObjectName(_fromUtf8("dock_segm_classif"))
        self.segmentation_classification_settings = QtGui.QWidget()
        self.segmentation_classification_settings.setObjectName(_fromUtf8("segmentation_classification_settings"))
        self.parameter_bttn = QtGui.QPushButton(self.segmentation_classification_settings)
        self.parameter_bttn.setGeometry(QtCore.QRect(70, 10, 151, 23))
        self.parameter_bttn.setObjectName(_fromUtf8("parameter_bttn"))
        self.dock_segm_classif.setWidget(self.segmentation_classification_settings)
        self.gridLayout_2.addWidget(self.dock_segm_classif, 0, 2, 1, 1)
        self.widget = QSignalDetectorWidget(self.widget_2)
        self.widget.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(300, 200))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout_5 = QtGui.QFormLayout(self.widget)
        self.formLayout_5.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.gridLayout_2.addWidget(self.widget, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.widget_2, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Detection Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.dock_segm_classif.setWindowTitle(QtGui.QApplication.translate("Dialog", "Segmentation and Classification Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.parameter_bttn.setText(QtGui.QApplication.translate("Dialog", "Parameters Measurement", None, QtGui.QApplication.UnicodeUTF8))
        self.widget.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Signal to learn about algorithm parameters</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

from graphic_interface.widgets.QSignalDetectorWidget import QSignalDetectorWidget
import icons_rc
