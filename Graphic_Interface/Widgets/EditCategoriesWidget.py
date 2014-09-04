from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QWidget

from Graphic_Interface.Windows.EditCategoryWidgetUI import Ui_EditCategoryWidget


class EditCategoriesWidget(Ui_EditCategoryWidget,QWidget):

    def __init__(self,parent=None,categoryName="",classificationData=None, selectionOnly=False):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        if not isinstance(categoryName,str) and not isinstance(categoryName,QtCore.QString):
            categoryName = self.tr(u"No Name Category")
        self.labelCategoryName.setText(u"<h2>"+self.tr(u"Category:")+u" "+categoryName+u"</h2>")

        self.labelCategoryName.setStyleSheet("background-color:#FFF")
        self.comboCategories.setStyleSheet("background-color:#DDF")
        self.lineEditCategoryValue.setStyleSheet("background-color:#DDF")

        for x in classificationData.getvalues(categoryName):
            self.comboCategories.addItem(x)

        if selectionOnly:
            self.bttnAddValue.setEnabled(False)
            self.bttnRemoveSelected.setEnabled(False)
            self.lineEditCategoryValue.setEnabled(False)

        self.categoryName = categoryName
        self.classificationData = classificationData

        self.bttnAddValue.clicked.connect(self.addValue)
        self.bttnRemoveSelected.clicked.connect(self.removeValue)

    def addValue(self):
        val = str(self.lineEditCategoryValue.text())
        if val == "":
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"), self.tr(u"The value for this category should have a name."))
            return
        if self.classificationData.addValue(self.categoryName,val):
            self.comboCategories.addItem(val)
            self.comboCategories.setCurrentIndex(self.comboCategories.count()-1)
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"), self.tr(u"There is other value with that name in the category"))

    def removeValue(self):
        if self.comboCategories.count() > 0:
            val = self.comboCategories.itemText(self.comboCategories.currentIndex())
            if self.classificationData.removeValue(self.categoryName,val):
                self.comboCategories.removeItem(self.comboCategories.currentIndex())
            else:
                QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"), self.tr(u"The value can't be removed because is in use."))
