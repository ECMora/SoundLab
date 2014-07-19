from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QWidget
from EditCategoryWidgetUI import Ui_EditCategoryWidget


class EditCategoriesWidget(Ui_EditCategoryWidget,QWidget):
    # valueAdded = pyqtSignal(str,str) #category, value
    # valueRemoved = pyqtSignal(str,str) #category, value

    def __init__(self,parent=None,categoryName="",categoryValues=[],tabooValues=[], selectionOnly=False):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        if not isinstance(categoryName,str) and not isinstance(categoryName,QtCore.QString):
            categoryName = "No Name Category"
        self.labelCategoryName.setText("Category: "+ categoryName)
        for x in categoryValues:
            self.comboCategories.addItem(x)

        if selectionOnly:
            self.bttnAddValue.setEnabled(False)
            self.bttnRemoveSelected.setEnabled(False)
            self.lineEditCategoryValue.setEnabled(False)

        self.categoryName = categoryName
        self.categoryValues = categoryValues
        self.tabooValues = tabooValues

        self.bttnAddValue.clicked.connect(self.addValue)
        self.bttnRemoveSelected.clicked.connect(self.removeValue)

    def addValue(self):
        val = self.lineEditCategoryValue.text()
        if val == "":
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "The value for this category should have a name.")
            return
        elif val in self.categoryValues:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "There is other value with that name in the category")
            return

        self.comboCategories.addItem(val)
        self.categoryValues.append(val)
        self.comboCategories.setCurrentIndex(self.comboCategories.count()-1)

    def removeValue(self):
        if self.comboCategories.count() > 0:
            val = self.comboCategories.itemText(self.comboCategories.currentIndex())
            if val not in self.tabooValues:
                self.categoryValues.remove(val)
                self.comboCategories.removeItem(self.comboCategories.currentIndex())
            else:
                QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Error", "The value can't be removed because is in use.")
