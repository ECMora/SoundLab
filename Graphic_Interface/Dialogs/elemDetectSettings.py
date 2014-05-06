from math import log10
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
import pyqtgraph as pg
from Duetto_Core.Segmentation.Detectors.ElementsDetectors.OneDimensionalElementsDetector import DetectionSettings, DetectionType,AutomaticThresholdType
from Graphic_Interface.Dialogs.ui_elemDetectSettings import Ui_Dialog


class ElemDetectSettingsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(QDialog,self).__init__(parent)
        self.setupUi(self)


        if parent is not None:
            self.widget.specgramSettings.NFFT = parent.widget.specgramSettings.NFFT
            self.widget.specgramSettings.overlap = parent.widget.specgramSettings.overlap
            self.widget.specgramSettings.window = parent.widget.specgramSettings.window
            self.widget.signalProcessor.signal = parent.widget.signalProcessor.signal
        else:
            self.widget.specgramSettings.overlap = 50
        self.detectortypeData = [DetectionType.LocalMax,DetectionType.LocalHoldTime,DetectionType.LocalMaxProportion,
                             DetectionType.IntervalRms,DetectionType.IntervalMaxMedia,DetectionType.IntervalMaxProportion,DetectionType.IntervalFrecuencies,
                             DetectionType.Envelope_Abs_Decay_Averaged,DetectionType.Envelope_Rms]

        self.detectionSettings = DetectionSettings(DetectionType.Envelope_Abs_Decay_Averaged,AutomaticThresholdType.Global_MaxMean)
        self.cmbxDetectionMethod.setCurrentIndex(7)

        self.cmbxDetectionMethod.currentIndexChanged.connect(self.changeDetectionMethod)

        self.widget.setSelectedTool("OscilogramThreshold")
        #spectrogram
        self.dsbxThresholdSpec.valueChanged.connect(self.detect)
        self.dsbxMinSizeFreq.valueChanged.connect(self.detect)
        self.dsbxminSizeTime.valueChanged.connect(self.detect)
        #oscillogram
        self.dsbxThreshold.valueChanged.connect(self.detect)
        self.dsbxThreshold.valueChanged.connect(self.updateThresholdLine)

        self.cbxSpectralSubelements.stateChanged.connect(self.updateGraphsVisibility)
        self.checboxAutomaticThreshold.stateChanged.connect(self.changeDetectionMethod)

        self.dsbxThreshold2.valueChanged.connect(self.detect)
        self.dsbxDecay.valueChanged.connect(self.detect)
        self.dsbxMinSize.valueChanged.connect(self.detect)
        self.dsbxMergeFactor.valueChanged.connect(self.detect)
        self.sbxSoftFactor.valueChanged.connect(self.detect)

        self.widget.visibleSpectrogram = False
        self.widget.visibleOscilogram = True
        self.widget.setEnvelopeVisibility(True)

        self.widget.signalProcessor.signal = self.widget.signalProcessor.signal.smallSignal()
        if self.widget.signalProcessor.signal is None:
            self.widget.open("Utils\\Didactic Signals\\recognition.wav")
        else:
            self.widget.mainCursor.min,self.widget.mainCursor.max = 0,len(self.widget.signalProcessor.signal.data)



        self.widget.axesOscilogram.setVisibleThreshold(True)

        self.widget.axesOscilogram.threshold.sigPositionChangeFinished.connect(self.updateThreshold)
        self.widget.axesOscilogram.threshold.setBounds((-2**(self.widget.signalProcessor.signal.bitDepth-1),2**(self.widget.signalProcessor.signal.bitDepth-1)))

        self.hist = pg.widgets.HistogramLUTWidget.HistogramLUTItem()
        self.hist.setImageItem(self.widget.axesSpecgram.imageItem)
        self.hist.region.lineMoved()
        self.hist.region.lineMoveFinished()


        self.widget.visualChanges = True
        self.widget.computeSpecgramSettings()
        self.widget.refresh()


    def changeDetectionMethod(self,text):
        self.detectionSettings.detectiontype = self.detectortypeData[self.cmbxDetectionMethod.currentIndex()]
        self.detectionSettings.automaticthresholdtype = AutomaticThresholdType.Global_MaxMean if  self.checboxAutomaticThreshold.isChecked() else AutomaticThresholdType.UserDefined

        self.detect()

    def updateGraphsVisibility(self):
        self.widget.visibleSpectrogram = self.cbxSpectralSubelements.isChecked()
        self.widget.refresh()


    def updateThreshold(self,line):
        self.dsbxThreshold.setValue(self.toDB() if line.value() == 0 else self.toDB(line.value()))

    def updateThresholdLine(self):
        self.widget.axesOscilogram.threshold.setValue(round((10.0**((60+self.dsbxThreshold.value())/20.0))*(2**self.widget.signalProcessor.signal.bitDepth)/1000.0,0)
                                                      *self.widget.envelopeFactor-2**(self.widget.signalProcessor.signal.bitDepth-1))



    def toDB(self,value=None):
        if value is None:
            return -60
        return -60 + int(20*log10(abs((value+2**(self.widget.signalProcessor.signal.bitDepth-1))/self.widget.envelopeFactor)*1000.0/(2**self.widget.signalProcessor.signal.bitDepth)))

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
        self.cbxmeasurementLocationCenter

    @pyqtSlot()
    def detect(self):
        self.widget.detectElements(threshold=abs(self.dsbxThreshold.value()),detectionsettings=self.detectionSettings, decay=self.dsbxDecay.value(), minSize= self.dsbxMinSize.value(), softfactor=self.sbxSoftFactor.value(), merge_factor=self.dsbxMergeFactor.value(),threshold2=abs(self.dsbxThreshold2.value())
        ,threshold_spectral=self.dsbxThresholdSpec.value(), minsize_spectral=(self.dsbxMinSizeFreq.value(),self.dsbxminSizeTime.value()),findSpectralSublements = self.cbxSpectralSubelements.isChecked())
        self.widget.refresh()



import re, sre_compile, sre_constants, sre_parse