from PyQt4 import QtCore, QtGui
from graphic_interface.widgets.EditCategoriesWidget import EditCategoriesWidget
from graphic_interface.windows.ui_python_files import EditCategoriesDialogUI as editCateg


class EditCategoriesDialog(editCateg.Ui_Dialog, QtGui.QDialog):
    """
    Dialog that allow to select and edit the classification data.
    Allow to edit the categories and values for classification.
    """

    def __init__(self, classificationData, selectionOnly=True):
        """

        :param classificationData:
        :param selectionOnly:
        :return:
        """
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.clasiffCategories_vlayout = QtGui.QVBoxLayout()

        self.classificationData = classificationData
        self.selection_widgets = []

        for k in self.classificationData.categories.keys():
            # foreach clasification category add a widget to show it
            widget = EditCategoriesWidget(self, k, self.classificationData, selectionOnly=selectionOnly)

            self.selection_widgets.append(widget)
            self.clasiffCategories_vlayout.addWidget(widget)

        # connect the methods for add category action
        self.bttnAddCategory.clicked.connect(self.addCategory)

        widget = QtGui.QWidget()
        widget.setLayout(self.clasiffCategories_vlayout)
        self.listWidget.setWidget(widget)

    def addCategory(self):
        dialog = QtGui.QDialog(self)
        dialog.setWindowTitle(self.tr(u"Create New Category"))
        layout = QtGui.QVBoxLayout()
        layout.addWidget(QtGui.QLabel(self.tr(u"Insert the name of the new Category")))
        text = QtGui.QLineEdit()
        layout.addWidget(text)
        butts = QtGui.QDialogButtonBox()

        butts.addButton(QtGui.QDialogButtonBox.Ok)
        butts.addButton(QtGui.QDialogButtonBox.Cancel)
        QtCore.QObject.connect(butts, QtCore.SIGNAL("accepted()"), dialog.accept)
        QtCore.QObject.connect(butts, QtCore.SIGNAL("rejected()"), dialog.reject)

        layout.addWidget(butts)
        dialog.setLayout(layout)
        if dialog.exec_():
            category = str(text.text())
            if category == "":
                QtGui.QMessageBox.warning(QtGui.QMessageBox(),
                                          self.tr(u"Error"), self.tr(u"Invalid Category Name."))
                return
            if self.clasiffCategories_vlayout and self.classificationData.addCategory(category):
                self.clasiffCategories_vlayout.addWidget(EditCategoriesWidget(self, category, self.classificationData))
