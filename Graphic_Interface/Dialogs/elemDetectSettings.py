from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
from Graphic_Interface.Dialogs.ui_elemDetectSettings import Ui_elemDetectSettingsDialog


class ElemDetectSettingsDialog(QDialog, Ui_elemDetectSettingsDialog):
    def __init__(self, parent, windowFlags=None):
        if windowFlags:
            QDialog.__init__(self, parent, windowFlags)
        else:
            QDialog.__init__(self, parent)
        self.setupUi(self)

    @pyqtSlot(bool)
    def on_chbxDetectOsc_toggled(self, checked):
        self.dsbxThreshold.setEnabled(checked)
        self.dsbxMinSize.setEnabled(checked)
        self.dsbxMergeFactor.setEnabled(checked)
        self.dsbxDecay.setEnabled(checked)
        self.sbxSoftFactor.setEnabled(checked)

    @pyqtSlot(bool)
    def on_chbxDetectSpec_toggled(self, checked):
        self.dsbxThresholdSpec.setEnabled(checked)
        self.chbxPercentileThreshold.setEnabled(checked)
        self.dsbxminSizeTime.setEnabled(checked)
        self.dsbxMinSizeFreq.setEnabled(checked)
        self.sbxMergeFactorTime.setEnabled(checked)
        self.sbxMergeFactorFreq.setEnabled(checked)

    @pyqtSlot(bool)
    def on_chbxPercentileThreshold_toggled(self, checked):
        if checked:
            self.dsbxThresholdSpec.setMinimum(0.01)
            self.dsbxThresholdSpec.setMaximum(99.99)
            self.dsbxThresholdSpec.setValue(98)
        else:
            self.dsbxThresholdSpec.setMinimum(0)
            self.dsbxThresholdSpec.setMaximum(500)
            self.dsbxThresholdSpec.setValue(100)

    def getSettings(self):
        return {'detectSpec': self.chbxDetectSpec.isChecked(),
                'percentileThreshold': self.chbxPercentileThreshold.isChecked(),
                'threshold': self.dsbxThresholdSpec.value(),
                'minSizeTime': self.dsbxminSizeTime.value(),
                'minSizeFreq': self.dsbxMinSizeFreq.value(),
                'mergeFactorTime': self.sbxMergeFactorTime.value(),
                'mergeFactorFreq': self.sbxMergeFactorFreq.value()}
