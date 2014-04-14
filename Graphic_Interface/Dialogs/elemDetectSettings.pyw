from math import log10
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
import pyqtgraph as pg
from Duetto_Core.AudioSignals.WavFileSignal import WavFileSignal
from Graphic_Interface.Dialogs.ui_elemDetectSettings import Ui_Dialog


class ElemDetectSettingsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(QDialog,self).__init__(parent)
        self.setupUi(self)
        self.widget.visibleSpectrogram = True
        self.widget.visibleOscilogram = True
        if parent is not None:
            self.widget.specgramSettings.NFFT = parent.widget.specgramSettings.NFFT
            self.widget.specgramSettings.overlap = parent.widget.specgramSettings.overlap
            self.widget.specgramSettings.window = parent.widget.specgramSettings.window



        #espectrogram
        self.dsbxThresholdSpec.valueChanged.connect(self.detect)
        self.dsbxMinSizeFreq.valueChanged.connect(self.detect)
        self.dsbxminSizeTime.valueChanged.connect(self.detect)
        #oscilogram
        self.dsbxThreshold.valueChanged.connect(self.detect)
        self.dsbxThreshold.valueChanged.connect(self.updateThresholdLine)


        self.dsbxThreshold2.valueChanged.connect(self.detect)
        self.dsbxDecay.valueChanged.connect(self.detect)
        self.dsbxMinSize.valueChanged.connect(self.detect)
        self.dsbxMergeFactor.valueChanged.connect(self.detect)
        self.sbxSoftFactor.valueChanged.connect(self.detect)
        self.widget.signalProcessor.signal = WavFileSignal("Utils\\Didactic Signals\\recognition.wav")
        self.widget.mainCursor.min,self.widget.mainCursor.max = 0,len(self.widget.signalProcessor.signal.data)
        self.widget.axesOscilogram.setVisibleThreshold(True)

        self.widget.axesOscilogram.threshold.sigPositionChangeFinished.connect(self.updateThreshold)
        self.widget.axesOscilogram.threshold.setBounds((0,2**(self.widget.signalProcessor.signal.bitDepth-1)))

        self.widget.visualChanges = True
        self.hist = pg.widgets.HistogramLUTWidget.HistogramLUTItem()
        self.hist.setImageItem(self.widget.axesSpecgram.imageItem)
        self.widget.refresh()

    def updateThreshold(self,line):
        self.dsbxThreshold.setValue(self.toDB() if line.value() == 0 else self.toDB(line.value()))

    def updateThresholdLine(self):
        self.widget.axesOscilogram.threshold.setValue(round((10.0**((60+self.dsbxThreshold.value())/20.0))*(2**self.widget.signalProcessor.signal.bitDepth)/1000.0,0))


    def toDB(self,value=None):
        if value is None:
            return -60
        return -60 + int(20*log10(abs(value)*1000.0/(2**self.widget.signalProcessor.signal.bitDepth)))

    def load_Theme(self,theme):
        self.theme = theme
        self.hist.region.setRegion(theme.histRange)
        self.hist.gradient.restoreState(theme.colorBarState)
        self.widget.load_Theme(theme)
        self.widget.visualChanges = True
        self.widget.refresh()
        self.hist.region.lineMoved()
        self.hist.region.lineMoveFinished()

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
        ,threshold_spectral=self.dsbxThresholdSpec.value(), minsize_spectral=(self.dsbxMinSizeFreq.value(),self.dsbxminSizeTime.value()),findSpectralSublements = False)
        self.widget.refresh()



import re, sre_compile, sre_constants, sre_parse