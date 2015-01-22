from PyQt4.QtGui import QDialog
from graphic_interface.windows.ui_python_files import InsertSilenceDialog as sdialog


class InsertSilenceDialog(sdialog.Ui_Dialog, QDialog):
    """
    Dialog to select a duration for a signal insertion.
    """

    # CONSTANTS
    # the static dictionary that memorize the dialog
    # element values during the application execution
    # region dialog elements values

    dialogValues = {
        "insertSpinBox": 5000
    }
    # endregion

    def __init__(self):
        """
        Initialize the dialogs elements with their last value
        """
        QDialog.__init__(self)
        self.setupUi(self)

        # load the previous selected values for the dialog or the defaults ones
        self.load_values()
        self.btonaceptar.clicked.connect(self.save_values)

    def load_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected filter type on radio buttons
        self.insertSpinBox.setValue(self.dialogValues["insertSpinBox"])

    def save_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected amplitude modulation type on radio buttons
        self.dialogValues["insertSpinBox"] = self.insertSpinBox.value()

