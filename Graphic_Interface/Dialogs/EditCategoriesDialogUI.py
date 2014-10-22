# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Biologia\DUETTO PROGRAMS\Sound Lab\DuettoSystem\graphic_interface\UI Files\EditCategoriesDialogUI.ui'
#
# Created: Sat Jul 19 21:57:43 2014
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
        Dialog.resize(355, 366)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.bttnAddCategory = QtGui.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bttnAddCategory.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/myappicons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bttnAddCategory.setIcon(icon)
        self.bttnAddCategory.setIconSize(QtCore.QSize(30, 30))
        self.bttnAddCategory.setObjectName(_fromUtf8("bttnAddCategory"))
        self.gridLayout.addWidget(self.bttnAddCategory, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.listWidget = QtGui.QScrollArea(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setStyleSheet(_fromUtf8(""))
        self.listWidget.setWidgetResizable(True)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.containerWidget = QtGui.QWidget()
        self.containerWidget.setGeometry(QtCore.QRect(0, 0, 335, 269))
        self.containerWidget.setObjectName(_fromUtf8("containerWidget"))
        self.listWidget.setWidget(self.containerWidget)
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.buttonBox.setFont(font)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Edit Categories", None, QtGui.QApplication.UnicodeUTF8))
        self.bttnAddCategory.setText(QtGui.QApplication.translate("Dialog", "Add Category ", None, QtGui.QApplication.UnicodeUTF8))

import graphic_interface.windows.icons_rc
