from PyQt4.QtGui import QDialog
from graphic_interface.windows.ui_python_files import FilterOptionsDialog as filterdg


class FilterDialog(filterdg.Ui_Dialog, QDialog):
    """
    Dialog to select a filter.
    """

    # CONSTANTS
    # the static dictionary that memorize the dialog
    # element values during the application execution

    # region dialog elements values
    dialogValues = {
        "rButtonLowPass": True,
        "rButtonHighPass": False,
        "rButtonBandPass": False,
        "rButtonBandStop": False,
        "spinBoxLowPass": 0.00,
        "spinBoxHighPass": 0.00,
        "spinBoxBandStopFu": 0.00,
        "spinBoxBandStopFl": 0.00,
        "spinBoxBandPassFl": 0.00,
        "spinBoxBandPassFu": 0.00
    }
    # endregion

    def __init__(self, signalSamplingRate=None):
        """
        Initialize the dialogs elements with their last value
        """
        QDialog.__init__(self)
        self.setupUi(self)

        # load the previous selected values for the dialog or the defaults ones
        self.load_values()
        self.btonaceptar.clicked.connect(self.save_values)

        # set the limits of the possible selectable frequencies to valid ranges
        self.spinBoxBandPassFl.valueChanged.connect(lambda value: self.spinBoxBandPassFu.setMinimum(value))
        self.spinBoxBandPassFu.valueChanged.connect(lambda value: self.spinBoxBandPassFl.setMaximum(value))

        self.spinBoxBandStopFl.valueChanged.connect(lambda value: self.spinBoxBandStopFu.setMinimum(value))
        self.spinBoxBandStopFu.valueChanged.connect(lambda value: self.spinBoxBandStopFl.setMaximum(value))

        if signalSamplingRate is not None:
            # max freq in kHz
            max_freq = signalSamplingRate / 2000.0
            print(max_freq)
            self.spinBoxBandPassFu.setMaximum(max_freq)
            self.spinBoxBandStopFu.setMaximum(max_freq)
            self.spinBoxHighPass.setMaximum(max_freq)
            self.spinBoxLowPass.setMaximum(max_freq)

    def load_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected filter type on radio buttons
        self.rButtonLowPass.setChecked(self.dialogValues["rButtonLowPass"])
        self.rButtonHighPass.setChecked(self.dialogValues["rButtonHighPass"])
        self.rButtonBandStop.setChecked(self.dialogValues["rButtonBandStop"])
        self.rButtonBandPass.setChecked(self.dialogValues["rButtonBandPass"])

        # set the values of every spin box with the kHz of frequency selection
        self.spinBoxLowPass.setValue(self.dialogValues["spinBoxLowPass"])
        self.spinBoxHighPass.setValue(self.dialogValues["spinBoxHighPass"])
        self.spinBoxBandStopFu.setValue(self.dialogValues["spinBoxBandStopFu"])
        self.spinBoxBandStopFl.setValue(self.dialogValues["spinBoxBandStopFl"])
        self.spinBoxBandPassFl.setValue(self.dialogValues["spinBoxBandPassFl"])
        self.spinBoxBandPassFu.setValue(self.dialogValues["spinBoxBandPassFu"])

    def save_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # save the values of the selected filter type on radio buttons
        self.dialogValues["rButtonLowPass"] = self.rButtonLowPass.isChecked()
        self.dialogValues["rButtonHighPass"] = self.rButtonHighPass.isChecked()
        self.dialogValues["rButtonBandStop"] = self.rButtonBandStop.isChecked()
        self.dialogValues["rButtonBandPass"] = self.rButtonBandPass.isChecked()

        # save the values of the spin box with the frequencies
        self.dialogValues["spinBoxLowPass"] = self.spinBoxLowPass.value()
        self.dialogValues["spinBoxHighPass"] = self.spinBoxHighPass.value()
        self.dialogValues["spinBoxBandStopFu"] = self.spinBoxBandStopFu.value()
        self.dialogValues["spinBoxBandStopFl"] = self.spinBoxBandStopFl.value()
        self.dialogValues["spinBoxBandPassFl"] = self.spinBoxBandPassFl.value()
        self.dialogValues["spinBoxBandPassFu"] = self.spinBoxBandPassFu.value()

