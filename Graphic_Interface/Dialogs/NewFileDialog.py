from PyQt4.QtGui import QDialog
from Graphic_Interface.Dialogs.ui_new_file_dialog import Ui_NewFileDialog


class NewFileDialog(QDialog, Ui_NewFileDialog):
    def __init__(self, parent, windowFlags=None):
        if windowFlags:
            QDialog.__init__(self, parent, windowFlags)
        else:
            QDialog.__init__(self, parent)
        self.setupUi(self)

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
