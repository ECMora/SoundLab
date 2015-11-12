from PyQt4.QtGui import QDialog
from PyQt4.QtCore import Qt
from graphic_interface.windows.ui_python_files import ChangeVolumeDialog as cvdialog


class ChangeVolumeDialog(cvdialog.Ui_Dialog, QDialog):
    """
    Dialog to select a time-amplitude modulation.
    """

    # CONSTANTS
    # the static dictionary that memorize the dialog
    # element values during the application execution

    # region dialog elements values

    dialogValues = {
        "rbuttonConst": True,
        "rbuttonFadeIn": False,
        "rbuttonFadeOut": False,
        "rbuttonNormalize": False,
        "spinboxConstValue": 1.00,
        "spinboxNormalizePercent": 50.00,
        "cboxModulationType": 0
    }
    # endregion

    def __init__(self, parent=None):
        """
        Initialize the dialogs elements with their last value
        """
        QDialog.__init__(self, parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.setupUi(self)

        # load the previous selected values for the dialog or the defaults ones
        self.load_values()
        self.buttonBox.accepted.connect(self.save_values)

    def load_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected filter type on radio buttons
        self.rbuttonConst.setChecked(self.dialogValues["rbuttonConst"])
        self.rbuttonFadeIn.setChecked(self.dialogValues["rbuttonFadeIn"])
        self.rbuttonFadeOut.setChecked(self.dialogValues["rbuttonFadeOut"])
        self.rbuttonNormalize.setChecked(self.dialogValues["rbuttonNormalize"])

        # set the values of every spin box with the previous or default selection
        self.spinboxConstValue.setValue(self.dialogValues["spinboxConstValue"])
        self.spinboxNormalizePercent.setValue(self.dialogValues["spinboxNormalizePercent"])
        self.cboxModulationType.setCurrentIndex(self.dialogValues["cboxModulationType"])

    def save_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected amplitude modulation type on radio buttons
        self.dialogValues["rbuttonConst"] = self.rbuttonConst.isChecked()
        self.dialogValues["rbuttonFadeIn"] = self.rbuttonFadeIn.isChecked()
        self.dialogValues["rbuttonFadeOut"] = self.rbuttonFadeOut.isChecked()
        self.dialogValues["rbuttonNormalize"] = self.rbuttonNormalize.isChecked()

        # set the values of the selected amplitude modulation
        self.dialogValues["spinboxConstValue"] = self.spinboxConstValue.value()
        self.dialogValues["spinboxNormalizePercent"] = self.spinboxNormalizePercent.value()
        self.dialogValues["cboxModulationType"] = self.cboxModulationType.currentIndex()


