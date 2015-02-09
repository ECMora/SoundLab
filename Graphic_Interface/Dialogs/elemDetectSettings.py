# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
from pyqtgraph.parametertree import Parameter,ParameterTree
from graphic_interface.windows.ui_python_files.detectElementsDialog import Ui_Dialog
from Utils.Utils import smallSignal
from sound_lab_core.Segmentation.Detectors.OneDimensional.EnvelopeMethods.AbsDecayEnvelopeDetector import \
    AbsDecayEnvelopeDetector
from sound_lab_core.Segmentation.Elements.OneDimensionalElements.OneDimensionalElement import \
    SpectralMeasurementLocation


class ElemDetectSettingsDialog(QDialog, Ui_Dialog):
    """
    Dialog that allow to the user to select
    the segmentation, parameter measurement and classification
    type that would be used on the process of a segment.
    Factory of detectors, parameter measurers and classifiers
    """

    def __init__(self, parent, signal=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        if signal is not None:
            self.widget.signal = smallSignal(signal)
            # else load a didactic signal

        # parameter tree to provide the measurement and parameter configuration into the dialog
        self.ParamTree = self.getParamTree()
        self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).sigTreeStateChanged.connect(self.detect)
        self.ParamTree.param(unicode(self.tr(u'Spectral Detection Settings'))).sigTreeStateChanged.connect(self.detect)
        self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Detection Method'))).sigTreeStateChanged.connect(self.changeDetectionMethod)
        self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Auto'))).sigTreeStateChanged.connect(self.changeDetectionMethod)

        self.parameterTree = ParameterTree()
        self.parameterTree.setAutoScroll(True)
        self.parameterTree.setFixedWidth(340)
        self.parameterTree.setHeaderHidden(True)
        self.parameterTree.setParameters(self.ParamTree, showTop=False)

        # temporal
        self.spectralMeasurementLocation = SpectralMeasurementLocation()

        lay1 = QtGui.QVBoxLayout()
        lay1.setMargin(0)
        lay1.addWidget(self.parameterTree)

        self.osc_settings_contents.setLayout(lay1)
        self.dock_settings.setFixedWidth(350)

        self.widget.visibleSpectrogram = False
        self.widget.visibleOscilogram = True

        self._detector = None
        self._classifier = None

        self.detect()

    def getParamTree(self):
        """
        :return: the param tree with the segmentation options
        """
        # region Detection Params Definition

        # Time And Spectral Medition Parameters
        # the medition parameters are defined here
        # are divided into time and spectral meditions
        # time are those parameters that are measured in time domain. ie Oscilogram
        # spectral meditions are measured on spectrogram
        params = [{u'name': unicode(self.tr(u'Temporal Detection Settings')), u'type': u'group', u'children': [
            {u'name': unicode(self.tr(u'Detection Method')), u'type': u'list',
             u'default': 0, u'values':
                [(unicode(self.tr(u'Envelope')), 0)]},
            {u'name': unicode(self.tr(u'Threshold (db)')), u'type': u'float', u'value': -40.00, u'step': 1},
            {u'name': unicode(self.tr(u'Auto')), u'type': u'bool', u'default': True, u'value': True},
            {u'name': unicode(self.tr(u'Min Size (ms)')), u'type': u'float', u'value': 2.00, u'step': 1},
            {u'name': unicode(self.tr(u'Decay (ms)')), u'type': u'float', u'value': 1.00, u'step': 0.5},
            {u'name': unicode(self.tr(u'Threshold 2(db)')), u'type': u'float', u'value': 0.00, u'step': 1},
            {u'name': unicode(self.tr(u'Soft Factor')), u'type': u'float', u'value': 6, u'step': 1},
            {u'name': unicode(self.tr(u'Merge Factor (%)')), u'type': u'float', u'value': 5.00, u'step': 1,
             u'limits': (0, 50)}
        ]},

                  {u'name': unicode(self.tr(u'Spectral Detection Settings')), u'type': u'group', u'children': [
                      {u'name': unicode(self.tr(u'Detect Spectral Subelements')), u'type': u'bool', u'default': False,
                       u'value': False},
                      {u'name': unicode(self.tr(u'Threshold (%)')), u'type': u'float', u'value': 95.00, u'step': 1,
                       u'limits': (0, 100)},
                      {u'name': unicode(self.tr(u'Minimum size')), u'type': u'group', u'children': [
                          {u'name': unicode(self.tr(u'Time (ms)')), u'type': u'float', u'value': 0.00, u'step': 1},
                          {u'name': unicode(self.tr(u'Frequency (kHz)')), u'type': u'float', u'value': 0.00,
                           u'step': 1}]}
                  ]},

                  {u'name': unicode(self.tr(u'Measurement Location')), u'type': u'group', u'children': [
                      {u'name': unicode(self.tr(u'Start')), u'type': u'bool', u'default': False, u'value': False},
                      {u'name': unicode(self.tr(u'Center')), u'type': u'bool', u'default': False, u'value': False},
                      {u'name': unicode(self.tr(u'End')), u'type': u'bool', u'default': False, u'value': False},
                      {u'name': unicode(self.tr(u'Quartile 25')), u'type': u'bool', u'default': False, u'value': False},
                      {u'name': unicode(self.tr(u'Mean')), u'type': u'bool', u'default': False, u'value': False},
                      {u'name': unicode(self.tr(u'Quartile 75')), u'type': u'bool', u'default': False,
                       u'value': False}]}
        ]

        timeMeditions = [
            [unicode(self.tr(u"Start(s)")), True, lambda x, d: x.startTime()],
            [unicode(self.tr(u"End(s)")), True, lambda x, d: x.endTime()],
            [unicode(self.tr(u"StartToMax(s)")), False, lambda x, d: x.distanceFromStartToMax()],
            [unicode(self.tr(u"Duration(s)")), True, lambda x, d: x.duration()],
        ]

        self.spectralMeditions = [
            [unicode(self.tr(u"Spectral Elems")), False, lambda x, d: x.spectralElements()],
            [unicode(self.tr(u"Peak Freq(Hz)")), False, lambda x, d: x.peakFreq(d)],
            [unicode(self.tr(u"Peak Amplitude(dB)")), False, lambda x, d: x.peakAmplitude(d)],
            [unicode(self.tr(u"Frequency")),
             [
                 [unicode(self.tr(u"Threshold (db)")), -20]
             ],
             [
                 [unicode(self.tr(u"Min Freq(Hz)")), False, lambda x, d: x.minFreq(d)],
                 [unicode(self.tr(u"Max Freq(Hz)")), False, lambda x, d: x.maxFreq(d)],
                 [unicode(self.tr(u"Band Width(Hz)")), False, lambda x, d: x.bandwidth(d)]
             ]
            ],
            [unicode(self.tr(u"Peaks")),
             [
                 [unicode(self.tr(u"Peaks Threshold (db)")), -20]
             ],
             [
                 [unicode(self.tr(u"Peaks Above")), False, lambda x, d: x.peaksAbove(d)],
             ]
            ]

        ]

        waveMeditions = [
            [unicode(self.tr(u"PeekToPeek(V)")), False, lambda x, d: x.peekToPeek()],
            [unicode(self.tr(u"RMS(V)")), False, lambda x, d: x.rms()],
        ]

        self.meditions = [(unicode(self.tr(u'Temporal Meditions')), timeMeditions), \
                          (unicode(self.tr(u'Spectral Meditions')), self.spectralMeditions), \
                          (unicode(self.tr(u'Waveform Meditions')), waveMeditions)]

        for name, dict in self.meditions:
            children = []
            for x in dict:
                if isinstance(x[1], bool):
                    children.append({u'name': x[0], u'type': u'bool', u'default': x[1], u'value': x[1]})
                else:
                    temp = []
                    for y in x[1]:
                        temp.append({u'name': y[0], u'type': u'float', u'value': y[1], u'step': 0.1})
                    for y in x[2]:
                        temp.append({u'name': y[0], u'type': u'bool', u'default': y[1], u'value': y[1]})
                    children.append({u'name': x[0], u'type': u'group', u'children': temp})
            params.append({u'name': name, u'type': u'group', u'children': children})

        # endregion

        return Parameter.create(name=u'params', type=u'group', children=params)

    def changeDetectionMethod(self,paramTree,changes):
        for param, change, data in changes:
            path = self.ParamTree.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()
            # if childName == unicode(self.tr(u'Temporal Detection Settings')) + u'.' +\
            #         unicode(self.tr(u'Detection Method')):
            #     self.detectionSettings.detectiontype = self.detectortypeData[data]
            # elif childName == unicode(self.tr(u'Temporal Detection Settings')) + u'.' + unicode(self.tr(u'Auto')):
            #     if data:
            #         self.detectionSettings.automaticthresholdtype = AutomaticThresholdType.Global_MaxMean
            #     else:
            #         self.detectionSettings.automaticthresholdtype = AutomaticThresholdType.UserDefined
        self.detect()

    def getspectralParameters(self):
        """
        obtain the methods for spectral parameter meausrement of the measurementLocations
        """
        params = []

        for x in self.spectralMeditions:
            if isinstance(x[1], bool):
                if x[1]:
                    if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.START][0]:
                        params.append([x[0] + "(start)", x[2], [["location", self.spectralMeasurementLocation.START]]])
                    if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.CENTER][0]:
                        params.append(
                            [x[0] + "(center)", x[2], [["location", self.spectralMeasurementLocation.CENTER]]])
                    if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.END][0]:
                        params.append([x[0] + "(end)", x[2], [["location", self.spectralMeasurementLocation.END]]])
                    if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE25][0]:
                        params.append(
                            [x[0] + "(quartile25)", x[2], [["location", self.spectralMeasurementLocation.QUARTILE25]]])
                    if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE75][0]:
                        params.append(
                            [x[0] + "(quartile75)", x[2], [["location", self.spectralMeasurementLocation.QUARTILE75]]])
            else:
                for y in x[2]:
                    if y[1]:
                        if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.START][0]:
                            l = [paramData for paramData in x[1]]
                            l.append(["location", self.spectralMeasurementLocation.START])
                            params.append([y[0] + "(start)", y[2], l])
                        if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.CENTER][0]:
                            l = [paramData for paramData in x[1]]
                            l.append(["location", self.spectralMeasurementLocation.CENTER])
                            params.append([y[0] + "(center)", y[2], l])
                        if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.END][0]:
                            l = [paramData for paramData in x[1]]
                            l.append(["location", self.spectralMeasurementLocation.END])
                            params.append([y[0] + "(end)", y[2], l])
                        if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE25][0]:
                            l = [paramData for paramData in x[1]]
                            l.append(["location", self.spectralMeasurementLocation.QUARTILE25])
                            params.append([y[0] + "(quartile25)", y[2], l])
                        if self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE75][0]:
                            l = [paramData for paramData in x[1]]
                            l.append(["location", self.spectralMeasurementLocation.QUARTILE75])
                            params.append([y[0] + "(quartile75)", y[2], l])

        return params

    def getSettings(self):
        # parameters
        for name, dict in self.meditions:
            for x in dict:
                if isinstance(x[1], bool):
                    x[1] = self.ParamTree.param(name).param(x[0]).value()
                else:
                    for y in x[1]:
                        y[1] = self.ParamTree.param(name).param(x[0]).param(y[0]).value()
                    for y in x[2]:
                        y[1] = self.ParamTree.param(name).param(x[0]).param(y[0]).value()

        # measurements u'Measurement Location'
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.START][0] = self.ParamTree.param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Start'))).value()
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.END][0] = self.ParamTree.param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'End'))).value()
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.CENTER][0] = self.ParamTree.param(
            unicode(self.tr(u'Measurement Location'))).param(unicode(self.tr(u'Center'))).value()
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE25][
            0] = self.ParamTree.param(unicode(self.tr(u'Measurement Location'))).param(
            unicode(self.tr(u'Quartile 25'))).value()
        self.spectralMeasurementLocation.MEDITIONS[self.spectralMeasurementLocation.QUARTILE75][
            0] = self.ParamTree.param(unicode(self.tr(u'Measurement Location'))).param(
            unicode(self.tr(u'Quartile 75'))).value()

    def getParameters(self):
        # todo create the list of parameters objects
        params = []
        for name, dict in self.meditions:
            if not name == unicode(self.tr(u'Spectral Meditions')):
                for x in dict:
                    if isinstance(x[1], bool):
                        if x[1]:
                            params.append([x[0], x[2], []])
                    else:
                        for y in x[2]:
                            if y[1]:
                                params.append([y[0], y[2], x[1]])
        return params + self.getspectralParameters()

    def getParametersList(self):
        """
        :return: The list pf parameters that would be measured
        """
        # (TEMPORAL) update from the tree parameter the parameters to measure
        self.getSettings()

        return self.getParameters()

    # region WorkSpace

    def load_workspace(self, workspace):
        """
        Method that loads the workspace to update visual options from main window.
        :param workspace:
        """
        self.widget.load_workspace(workspace)

    # endregion

    # region Detector, Parameter Measurers and Classifier

    @property
    def detector(self):
        """
        :return: The selected detector to perform segmentation
        """

        # get the detector's parameters manually
        # TODO the concrete implementation must be changed dinamically
        threshold = self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(
            unicode(self.tr(u'Threshold (db)'))).value()

        decay = self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(
            unicode(self.tr(u'Decay (ms)'))).value()

        min_size = self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(
            unicode(self.tr(u'Min Size (ms)'))).value()

        softfactor = self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(
            unicode(self.tr(u'Soft Factor'))).value()

        merge_factor = self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(
            unicode(self.tr(u'Merge Factor (%)'))).value()

        # create manually the detector
        self._detector = AbsDecayEnvelopeDetector(self.widget.signal, decay, threshold, min_size, merge_factor,
                                                 softfactor)
        return self._detector

    @detector.setter
    def detector(self, value):
        self._detector = value

    @property
    def measurerList(self):
        """
        :return: The list of selected parameters to measure
        """
        return self.getParameters()

    @property
    def classifier(self):
        return self._classifier

    @classifier.setter
    def classifier(self, value):
        self._classifier = value

    # endregion

    @pyqtSlot()
    def detect(self):
        """
        :return:
        """
        self.widget.detector = self.detector

        self.widget.detectElements()

        self.widget.graph()