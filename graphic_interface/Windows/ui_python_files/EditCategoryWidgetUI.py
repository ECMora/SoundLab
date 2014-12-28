# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Biologia\DUETTO PROGRAMS\Sound Lab\DuettoSystem\graphic_interface\UI Files\EditCategoryWidgetUI.ui'
#
# Created: Sun Jul 20 10:59:16 2014
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_EditCategoryWidget(object):
    def setupUi(self, EditCategoryWidget):
        EditCategoryWidget.setObjectName(_fromUtf8("EditCategoryWidget"))
        EditCategoryWidget.resize(305, 109)
        self.gridLayout = QtGui.QGridLayout(EditCategoryWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.bttnRemoveSelected = QtGui.QPushButton(EditCategoryWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bttnRemoveSelected.sizePolicy().hasHeightForWidth())
        self.bttnRemoveSelected.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/cerrar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bttnRemoveSelected.setIcon(icon)
        self.bttnRemoveSelected.setIconSize(QtCore.QSize(25, 25))
        self.bttnRemoveSelected.setObjectName(_fromUtf8("bttnRemoveSelected"))
        self.gridLayout.addWidget(self.bttnRemoveSelected, 2, 2, 1, 1)
        self.comboCategories = QtGui.QComboBox(EditCategoryWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboCategories.sizePolicy().hasHeightForWidth())
        self.comboCategories.setSizePolicy(sizePolicy)
        self.comboCategories.setObjectName(_fromUtf8("comboCategories"))
        self.gridLayout.addWidget(self.comboCategories, 2, 3, 1, 1)
        self.lineEditCategoryValue = QtGui.QLineEdit(EditCategoryWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditCategoryValue.sizePolicy().hasHeightForWidth())
        self.lineEditCategoryValue.setSizePolicy(sizePolicy)
        self.lineEditCategoryValue.setObjectName(_fromUtf8("lineEditCategoryValue"))
        self.gridLayout.addWidget(self.lineEditCategoryValue, 4, 3, 1, 1)
        self.bttnAddValue = QtGui.QPushButton(EditCategoryWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bttnAddValue.sizePolicy().hasHeightForWidth())
        self.bttnAddValue.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bttnAddValue.setIcon(icon1)
        self.bttnAddValue.setIconSize(QtCore.QSize(25, 25))
        self.bttnAddValue.setObjectName(_fromUtf8("bttnAddValue"))
        self.gridLayout.addWidget(self.bttnAddValue, 4, 2, 1, 1)
        self.labelCategoryName = QtGui.QLabel(EditCategoryWidget)
        self.labelCategoryName.setText(_fromUtf8(""))
        self.labelCategoryName.setObjectName(_fromUtf8("labelCategoryName"))
        self.gridLayout.addWidget(self.labelCategoryName, 1, 2, 1, 2)

        self.retranslateUi(EditCategoryWidget)
        QtCore.QMetaObject.connectSlotsByName(EditCategoryWidget)

    def retranslateUi(self, EditCategoryWidget):
        EditCategoryWidget.setWindowTitle(QtGui.QApplication.translate("EditCategoryWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.bttnRemoveSelected.setText(QtGui.QApplication.translate("EditCategoryWidget", "Remove Value", None, QtGui.QApplication.UnicodeUTF8))
        self.bttnAddValue.setText(QtGui.QApplication.translate("EditCategoryWidget", "AddValue", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
