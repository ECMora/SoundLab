# -*- coding: utf-8 -*-
from PyQt4.QtGui import QDialog

from graphic_interface.windows.ui_python_files.ui_new_file_dialog import Ui_NewFileDialog


class NewFileDialog(QDialog, Ui_NewFileDialog):
    # CONSTANTS
    # the static dictionary that memorize the dialog
    # element values during the application execution
    # region dialog elements values

    dialogValues = {
        "rbtnSilence": True,
        "rbtnWhiteNoise": False,
        "cbxBitDepth": 1,
        "dsbxDuration": 1,
        "sbxSamplingRate": 44100
    }
    # endregion

    def __init__(self, parent, windowFlags=None):
        if windowFlags:
            QDialog.__init__(self, parent, windowFlags)
        else:
            QDialog.__init__(self, parent)
        self.setupUi(self)

        # load the previous selected values for the dialog or the defaults ones
        self.load_values()
        self.buttonBox.accepted.connect(self.save_values)

    def load_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected type elements
        self.rbtnSilence.setChecked(self.dialogValues["rbtnSilence"])
        self.rbtnWhiteNoise.setChecked(self.dialogValues["rbtnWhiteNoise"])
        self.cbxBitDepth.setCurrentIndex(self.dialogValues["cbxBitDepth"])
        self.dsbxDuration.setValue(self.dialogValues["dsbxDuration"])
        self.sbxSamplingRate.setValue(self.dialogValues["sbxSamplingRate"])

    def save_values(self):
        """
        Load into the dialog elements the previously
        or default values.
        """

        # set the values of the selected amplitude modulation type on radio buttons
        self.dialogValues["rbtnSilence"] = self.rbtnSilence.isChecked()
        self.dialogValues["rbtnWhiteNoise"] = self.rbtnWhiteNoise.isChecked()
        self.dialogValues["cbxBitDepth"] = self.cbxBitDepth.currentIndex()
        self.dialogValues["dsbxDuration"] = self.dsbxDuration.value()
        self.dialogValues["sbxSamplingRate"] = self.sbxSamplingRate.value()


    @property
    def SamplingRate(self):
        return self.sbxSamplingRate.value()

    @property
    def Duration(self):
        return self.dsbxDuration.value()

    @property
    def BitDepth(self):
        return 1 << (self.cbxBitDepth.currentIndex() + 3)

    @property
    def Silence(self):
        return self.rbtnSilence.isChecked()

    @property
    def WhiteNoise(self):
        return self.rbtnWhiteNoise.isChecked()
