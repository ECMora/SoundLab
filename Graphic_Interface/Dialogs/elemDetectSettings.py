from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
from Graphic_Interface.Dialogs.ui_elemDetectSettings import Ui_Dialog


class ElemDetectSettingsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        self.setupUi(self)
        self.widgetOscilogram.visibleSpectrogram = False
        self.widgetSpecgram.visibleOscilogram = False

        #espectrogram
        self.dsbxThresholdSpec.valueChanged.connect(self.detectSpectrogram)
        self.dsbxMinSizeFreq.valueChanged.connect(self.detectSpectrogram)
        self.dsbxminSizeTime.valueChanged.connect(self.detectSpectrogram)
        self.sbxMergeFactorTime.valueChanged.connect(self.detectSpectrogram)
        self.sbxMergeFactorFreq.valueChanged.connect(self.detectSpectrogram)

        #oscilogram
        self.dsbxThreshold.valueChanged.connect(self.detectOscilogram)
        self.dsbxThreshold2.valueChanged.connect(self.detectOscilogram)
        self.dsbxDecay.valueChanged.connect(self.detectOscilogram)
        self.dsbxMinSize.valueChanged.connect(self.detectOscilogram)
        self.dsbxMergeFactor.valueChanged.connect(self.detectOscilogram)
        self.sbxSoftFactor.valueChanged.connect(self.detectOscilogram)


    @pyqtSlot(bool)
    def on_chbxDetectOsc_toggled(self, checked):
        self.dsbxThreshold.setEnabled(checked)
        self.dsbxThreshold2.setEnabled(checked)
        self.dsbxMinSize.setEnabled(checked)
        self.dsbxMergeFactor.setEnabled(checked)
        self.dsbxDecay.setEnabled(checked)
        self.sbxSoftFactor.setEnabled(checked)

    @pyqtSlot(bool)
    def on_chbxDetectSpec_toggled(self, checked):
        self.dsbxThresholdSpec.setEnabled(checked)
        self.dsbxminSizeTime.setEnabled(checked)
        self.dsbxMinSizeFreq.setEnabled(checked)
        self.sbxMergeFactorTime.setEnabled(checked)
        self.sbxMergeFactorFreq.setEnabled(checked)

    @pyqtSlot()
    def detectOscilogram(self):
        self.widgetOscilogram.detectElementsInOscilogram()

    @pyqtSlot()
    def detectSpectrogram(self):
        self.widgetSpecgram.detectElementsInEspectrogram()

import re, sre_compile, sre_constants, sre_parse