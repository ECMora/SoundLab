# -*- coding: utf-8 -*-
from math import log10

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
from pyqtgraph.parametertree import ParameterTree

from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import DetectionSettings, DetectionType,AutomaticThresholdType
from graphic_interface.windows.ui_python_files.ui_elemDetectSettings import Ui_Dialog


class ElemDetectSettingsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, paramTree):
        super(QDialog,self).__init__(parent)
        self.setupUi(self)

        if parent is not None:
            self.widget.axesSpecgram
            self.widget.signal = parent.widget.signal


        self.detectortypeData = [DetectionType.LocalMax,
                             DetectionType.IntervalRms,DetectionType.IntervalMaxMedia,
                             DetectionType.IntervalMaxProportion,
                             DetectionType.Envelope_Abs_Decay_Averaged,
                             DetectionType.Envelope_Rms]

        self.detectionSettings = DetectionSettings(DetectionType.Envelope_Abs_Decay_Averaged,AutomaticThresholdType.Global_MaxMean)

        self.ParamTree = paramTree
        self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).sigTreeStateChanged.connect(self.detect)
        self.ParamTree.param(unicode(self.tr(u'Spectral Detection Settings'))).sigTreeStateChanged.connect(self.detect)
        self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Detection Method'))).sigTreeStateChanged.connect(self.changeDetectionMethod)
        self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Threshold (db)'))).sigTreeStateChanged.connect(self.updateThresholdLine)
        self.ParamTree.param(unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Detect Spectral Subelements'))).sigTreeStateChanged.connect(self.updateGraphsVisibility)
        self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Auto'))).sigTreeStateChanged.connect(self.changeDetectionMethod)
        self.parameterTree = ParameterTree()
        self.parameterTree.setAutoScroll(True)
        self.parameterTree.setFixedWidth(340)

        self.parameterTree.setHeaderHidden(True)
        self.parameterTree.setParameters(self.ParamTree, showTop=False)

        lay1 = QtGui.QVBoxLayout()
        lay1.setMargin(0)
        lay1.addWidget(self.parameterTree)

        self.osc_settings_contents.setLayout(lay1)
        # self.dock_settings.setVisible(False)
        self.dock_settings.setFixedWidth(350)

        self.widget.visibleSpectrogram = False
        self.widget.visibleOscilogram = True


        self.widget.signal = self.widget.signal.smallSignal()
        if self.widget.signal is None:
            self.widget.open("Utils\\Didactic Signals\\recognition.wav")

        # self.widget.axesOscilogram.threshold.sigPositionChangeFinished.connect(self.updateThreshold)
        # self.widget.axesOscilogram.threshold.setBounds((-2**(self.widget.signalProcessor.signal.bitDepth-1),2**(self.widget.signalProcessor.signal.bitDepth-1)))

        self.detect()

    def changeDetectionMethod(self,paramTree,changes):
        for param, change, data in changes:
            path = self.ParamTree.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()
            if childName == unicode(self.tr(u'Temporal Detection Settings')) + u'.' +\
                    unicode(self.tr(u'Detection Method')):
                self.detectionSettings.detectiontype = self.detectortypeData[data]
            elif childName == unicode(self.tr(u'Temporal Detection Settings')) + u'.' + unicode(self.tr(u'Auto')):
                if data:
                    self.detectionSettings.automaticthresholdtype = AutomaticThresholdType.Global_MaxMean
                else:
                    self.detectionSettings.automaticthresholdtype = AutomaticThresholdType.UserDefined
        self.detect()

    def updateGraphsVisibility(self):
        self.widget.visibleSpectrogram = self.ParamTree.param(unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Detect Spectral Subelements'))).value()
        self.widget.refresh()

    def updateThreshold(self,line):
        self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Threshold (db)'))).setValue(self.toDB() if line.value() == 0 else self.toDB(line.value()))

    def updateThresholdLine(self):
        thresholdValue = self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Threshold (db)'))).value()
        self.widget.axesOscilogram.threshold.setValue(round((10.0**((60 + thresholdValue)/20.0))*(2**self.widget.signalProcessor.signal.bitDepth)/1000.0,0)
                                                      *self.widget.envelopeFactor-2**(self.widget.signalProcessor.signal.bitDepth-1))

    def toDB(self,value=None):
        if value is None:
            return -60
        return -60 + int(20*log10(abs((value+2**(self.widget.signalProcessor.signal.bitDepth-1))/self.widget.envelopeFactor)*1000.0/(2**self.widget.signalProcessor.signal.bitDepth)))

    def load_Theme(self,theme):
        self.theme = theme
        self.widget.load_Theme(theme)
        self.widget.graph()

    @pyqtSlot()
    def detect(self):
        self.widget.detectElements(threshold= self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Threshold (db)'))).value(),
                                   detectionsettings=self.detectionSettings,
                                   decay=self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Decay (ms)'))).value(),
                                   minSize= self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Min Size (ms)'))).value(),
                                   softfactor = self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Soft Factor'))).value(),
                                   merge_factor = self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Merge Factor (%)'))).value(),
                                   threshold2 = self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Threshold 2(db)'))).value(),
                                   threshold_spectral = self.ParamTree.param(unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Threshold (%)'))).value(),
                                   minsize_spectral=(self.ParamTree.param(unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Minimum size'))).param(unicode(self.tr(u'Frequency (kHz)'))).value(),
                                                     self.ParamTree.param(unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Minimum size'))).param(unicode(self.tr(u'Time (ms)'))).value()),
                                   findSpectralSublements = self.ParamTree.param(unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Detect Spectral Subelements'))).value())
        self.widget.refresh()



