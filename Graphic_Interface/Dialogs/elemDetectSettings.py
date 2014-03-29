from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Graphic_Interface.Dialogs.ui_elemDetectSettings import Ui_Dialog


class ElemDetectSettingsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(QDialog,self).__init__(parent)
        self.setupUi(self)
        self.widget.visibleSpectrogram = True
        self.widget.visibleOscilogram = True

        #espectrogram
        self.dsbxThresholdSpec.valueChanged.connect(self.detect)
        self.dsbxMinSizeFreq.valueChanged.connect(self.detect)
        self.dsbxminSizeTime.valueChanged.connect(self.detect)
        self.sbxMergeFactorTime.valueChanged.connect(self.detect)
        self.sbxMergeFactorFreq.valueChanged.connect(self.detect)
        #oscilogram
        self.dsbxThreshold.valueChanged.connect(self.detect)

        self.dsbxThreshold2.valueChanged.connect(self.detect)
        self.dsbxDecay.valueChanged.connect(self.detect)
        self.dsbxMinSize.valueChanged.connect(self.detect)
        self.dsbxMergeFactor.valueChanged.connect(self.detect)
        self.sbxSoftFactor.valueChanged.connect(self.detect)
        self.widget.signalProcessor.signal = WavFileSignal("Didactic Signals\\recognition.wav")
        self.widget.mainCursor.min,self.widget.mainCursor.max = 0,len(self.widget.signalProcessor.signal.data)
        self.widget.axesOscilogram.setVisibleThreshold(True)
        self.widget.visualChanges = True
        self.widget.refresh()


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
    def detect(self):
        self.widget.detectElements(threshold=abs(self.dsbxThreshold.value()), decay=self.dsbxDecay.value(), minSize= self.dsbxMinSize.value(), softfactor=self.sbxSoftFactor.value(), merge_factor=self.dsbxMergeFactor.value(),threshold2=abs(self.dsbxThreshold2.value())
        ,threshold_spectral=self.dsbxThresholdSpec.value(), minsize_spectral=(self.dsbxMinSizeFreq.value(),self.dsbxminSizeTime.value()),
               merge_factor_spectral=(self.sbxMergeFactorFreq.value(),self.sbxMergeFactorTime.value()))
        self.widget.refresh()



import re, sre_compile, sre_constants, sre_parse