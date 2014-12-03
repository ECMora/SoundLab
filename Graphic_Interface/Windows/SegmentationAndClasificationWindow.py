# -*- coding: utf-8 -*-
from math import log10
import os.path

from PyQt4.QtCore import pyqtSlot, Qt
import PyQt4.QtCore as QtCore
from PyQt4 import QtGui
from matplotlib import mlab
import xlwt
import numpy as np
from PyQt4.QtGui import QFileDialog, QAbstractItemView, QWidget
from pyqtgraph.parametertree import Parameter
from duetto.audio_signals.AudioSignal import AudioSignal

from sound_lab_core.Clasification.ClassificationData import ClassificationData
from sound_lab_core.Segmentation.Detectors.ElementsDetectors.OneDimensional.OneDimensionalElementsDetector import \
    DetectionType, AutomaticThresholdType, DetectionSettings
from sound_lab_core.Segmentation.Detectors.ElementsDetectors.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector
from sound_lab_core.Segmentation.Elements.Element import Element
from sound_lab_core.Segmentation.Elements.OneDimensionalElement import SpectralMeasurementLocation
from ..dialogs.elemDetectSettings import ElemDetectSettingsDialog
from graphic_interface.windows.TwoDimensionalAnalisysWindow import TwoDimensionalAnalisysWindow
from SegmentationAndClasificationWindowUI import Ui_MainWindow
import graphic_interface.dialogs.EditCategoriesDialogUI as editCateg
from graphic_interface.dialogs.EditCategoriesDialog import EditCategoriesDialog
from graphic_interface.widgets.EditCategoriesWidget import EditCategoriesWidget


class SegmentationAndClasificationWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    Class that process the segmentation and classification of a signal
    Contains a QSignalDetectorWidget that wrapper several functionalities
    Allows to select the segmentations and clasifications settings,
    and parameter measurement for detected segments.
    Provides a table for visualization of segment and measures,
    A two dimensional window to graph two measured params. One for each axis.
    Options for selection and visualization of segments
    Provides options for save the meditions to excell.
    """

    def __init__(self, parent=None, signal=None, classifcationSettings=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setupUi(self)
        #signal that the window will display
        if not signal:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"There is no signal to analyze."))
        if len(signal.data) / signal.samplingRate > 60:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The signal has more than 1 min of duration.") + " \n" +
                                      self.tr(u"Use the splitter to divide it"))
            self.close()
            self.rejectSignal = True
            return

        assert isinstance(signal, AudioSignal)
        self.widget.signalProcessor.signal = signal

        #TODO Parche que limita la obtencion de los parametros del spectrogram
        if parent is not None:
            self.widget.specgramSettings.NFFT = parent.widget.specgramSettings.NFFT
            self.widget.specgramSettings.overlap = parent.widget.specgramSettings.overlap
            self.widget.specgramSettings.window = parent.widget.specgramSettings.window
            self.widget.specgramSettings.visualOverlap = parent.widget.specgramSettings.visualOverlap
            if self.widget.specgramSettings.overlap < 0:
                if parent.widget.specgramSettings.visualOverlap < parent.widget.specgramSettings.NFFT:
                    self.widget.specgramSettings.overlap = parent.widget.specgramSettings.visualOverlap * 100.0 / parent.widget.specgramSettings.NFFT
                else:
                    self.widget.specgramSettings.overlap = 50

        self.widget.mainCursor.min = 0
        self.widget.mainCursor.max = len(self.widget.signalProcessor.signal.data)

        self.widget.computeSpecgramSettings(self.widget.specgramSettings.overlap)

        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True

        self.widget.graph()

        self.rejectSignal = False
        self.widget.mainCursor.min, self.widget.mainCursor.max = 0, len(self.widget.signalProcessor.signal.data)
        self.dockWidgetParameterTableOscilogram.setVisible(False)
        self.tableParameterOscilogram.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.show()

        #diferent colors for the even and odds rows in the parameter table and segment colors.
        self.parameterTable_rowcolor_odd, self.parameterTable_rowcolor_even = QtGui.QColor(0, 0, 255,
                                                                                           150), QtGui.QColor(0, 255, 0,
                                                                                                              150)
        self.algorithmDetectorSettings = DetectionSettings(DetectionType.Envelope_Abs_Decay_Averaged,
                                                           AutomaticThresholdType.Global_MaxMean)

        self.spectralMeasurementLocation = SpectralMeasurementLocation()
        self.widget.axesOscilogram.threshold.sigPositionChangeFinished.connect(self.updateThreshold)
        self.widget.axesOscilogram.threshold.setBounds((-2 ** (self.widget.signalProcessor.signal.bitDepth - 1),
                                                        2 ** (self.widget.signalProcessor.signal.bitDepth - 1)))
        self.detectionSettings = {"Threshold": -40, "Threshold2": 0, "MergeFactor": 5, "MinSize": 1, "Decay": 1,
                                  "SoftFactor": 6, "ThresholdSpectral": 95, "minSizeTimeSpectral": 0,
                                  "minSizeFreqSpectral": 0}
        #region Medition Definitions
        #Time And Spectral Medition Parameters
        # the medition parameters are defined here
        # are divided into time and spectral meditions
        # time are those parameters that are measured in time domain. ie Oscilogram
        #spectral meditions are measured on spectrogram
        params = [{u'name': unicode(self.tr(u'Temporal Detection Settings')), u'type': u'group', u'children': [
            {u'name': unicode(self.tr(u'Detection Method')), u'type': u'list',
             u'default': DetectionType.Envelope_Abs_Decay_Averaged, u'values':
                [(unicode(self.tr(u'Local Max')), DetectionType.LocalMax),
                 (unicode(self.tr(u'Interval Rms')), DetectionType.IntervalRms),
                 (unicode(self.tr(u'Interval Max Media')), DetectionType.IntervalMaxMedia),
                 (unicode(self.tr(u'Interval Max Proportion')), DetectionType.IntervalMaxProportion),
                 (unicode(self.tr(u'Envelope Abs Decay Averaged')), DetectionType.Envelope_Abs_Decay_Averaged),
                 (unicode(self.tr(u'Envelope Rms')), DetectionType.Envelope_Rms)]},
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


        self.timeMeditions = [
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

        self.waveMeditions = [
            [unicode(self.tr(u"PeekToPeek(V)")), False, lambda x, d: x.peekToPeek()],
            [unicode(self.tr(u"RMS(V)")), False, lambda x, d: x.rms()],
        ]

        self.meditions = [( unicode(self.tr(u'Temporal Meditions')), self.timeMeditions), \
                          (unicode(self.tr(u'Spectral Meditions')), self.spectralMeditions), \
                          (unicode(self.tr(u'Waveform Meditions')), self.waveMeditions)]
        #endregion

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

        #endregion

        #parameter tree to provide the medition and parameter configuration into the dialog
        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)

        #the spectral parameters that changes in function of the location measurements
        #funciones que reciben un elemento spectral 2 dimensiones y devuelven el valor del parametro medido
        #the order of the elements in the array of self.parameterMeasurement["Temporal"] is relevant for the visualization in the table and the
        #binding to the checkboxes in the dialog of parameter measurement
        self.widget.axesSpecgram.PointerSpecChanged.connect(self.updateStatusBar)
        self.widget.axesOscilogram.PointerOscChanged.connect(self.updateStatusBar)
        separator, separator1, separator2, separator3, separator4 = QtGui.QAction(self), QtGui.QAction(self), \
                                                                    QtGui.QAction(self), QtGui.QAction(self), \
                                                                    QtGui.QAction(self)

        separator.setSeparator(True)
        separator1.setSeparator(True)
        separator2.setSeparator(True)
        separator3.setSeparator(True)
        separator4.setSeparator(True)

        self.widget.createContextCursor(
            [self.actionZoomIn, self.actionZoom_out, self.actionZoom_out_entire_file, separator1, self.actionCombined,
             self.actionOscilogram, self.actionSpectogram,
             separator, self.actionClear_Meditions, self.actionMeditions, self.actionView_Parameters, separator2,
             self.actionZoom_Cursor, self.actionPointer_Cursor, self.actionRectangular_Cursor,
             self.actionRectangular_Eraser,
             separator3, self.actionDeselect_Elements, self.actionDelete_Selected_Elements, separator4,
             self.actionOsgram_Image, self.actionSpecgram_Image, self.actionCombined_Image])
        self.windowProgressDetection = QtGui.QProgressBar(self.widget)
        self.actionSignalName.setText(self.widget.signalName())

        #array of windows with two dimensional graphs. Are stored for a similar behavior to the one dimensional
        #in the main window. Updates the graphs
        self.twodimensionalGraphs = []

        # stores the measured parameters of the sdetected elements
        self.measuredParameters = np.array([[], []])

        self.classificationData = classifcationSettings if classifcationSettings is not None else ClassificationData()
        self.classificationData.valueAdded.connect(self.classificationCategoryValueAdded)
        self.classificationData.valueRemoved.connect(self.classificationCategoryValueRemove)
        self.classificationData.categoryAdded.connect(self.classificationCategoryAdded)

        #stores the classification data that are present in the table of meditions
        #has the form of a list with [["category name","category value"]] for each element
        # example with 2 elements and 2 categories
        # [[["Specie","Cartacuba"],["Location","Cuba"]],
        # [["Specie","Sinsonte"],["Location","Camaguey"]]]
        self.elementsClasificationTableData = []


        #the names of the columns in the table of parameters measured
        self.columnNames = []
        self.widget.histogram.setImageItem(self.widget.axesSpecgram.imageItem)

    #region Two Dimensional Graphs

    @pyqtSlot()
    def on_actionTwo_Dimensional_Graphs_triggered(self):
        """
        Creates a new two dimensional window for analysis.
        :return:
        """
        #a two dim window must create after segment detection and parameters measurement
        if self.tableParameterOscilogram.rowCount() == 0:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"There is not detected elements.") + u" \n" + self.tr(
                                          u"The two dimensional analisys requires at least one detected element."))
            return
        if self.tableParameterOscilogram.columnCount() == 0:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"There is not parameters measurement.") + u"\n" + self.tr(
                                          u"The two dimensional analisys requires at least one parameter measured."))
            return

        wnd = TwoDimensionalAnalisysWindow(self, columns=self.columnNames, data=self.measuredParameters,
                                           classificationData=self.classificationData)

        #connect the signals for update selection of elements detected
        wnd.elementSelected.connect(self.elementSelectedInTable)
        if self.theme:
            wnd.load_Theme(self.theme)

        if len(self.twodimensionalGraphs) > 0:
            wnd.selectElement(self.twodimensionalGraphs[0].previousSelectedElement)

        self.twodimensionalGraphs.append(wnd)
        wnd.elementsClasification.connect(self.elementsClasification)

    #endregion

    @QtCore.pyqtSlot(int, int, int)
    def on_widget_rangeChanged(self, left, right, total):
        self.horizontalScrollBar.blockSignals(True)
        self.horizontalScrollBar.setValue(0)
        self.horizontalScrollBar.setMinimum(0)
        self.horizontalScrollBar.setMaximum(total - (right - left))
        self.horizontalScrollBar.setValue(left)
        self.horizontalScrollBar.setPageStep(right - left)
        self.horizontalScrollBar.setSingleStep((right - left) / 16)
        self.horizontalScrollBar.blockSignals(True)
        self.horizontalScrollBar.blockSignals(False)

    def updateStatusBar(self, line):
        """
        :param line:
        """
        self.statusbar.showMessage(line)

    @QtCore.pyqtSlot(int)
    def on_horizontalScrollBar_valueChanged(self, value):
        self.widget.changeRange(value, value + self.horizontalScrollBar.pageStep(), emit=False)

    @pyqtSlot()
    def on_actionFull_Screen_triggered(self):
        """
        Switch the visualization of the window in fullscreen-normal.
        """
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()

    #region Tools
    @pyqtSlot()
    def on_actionZoom_Cursor_triggered(self):
        """


        """
        if self.actionZoom_Cursor.isChecked():
            self.actionPointer_Cursor.setChecked(False)
            self.actionRectangular_Cursor.setChecked(False)
            self.actionRectangular_Eraser.setChecked(False)
            # self.widget.setSelectedTool(Tools.Zoom)
        else:
            self.actionZoom_Cursor.setChecked(True)

    @pyqtSlot()
    def on_actionPointer_Cursor_triggered(self):
        if self.actionPointer_Cursor.isChecked():
            self.actionZoom_Cursor.setChecked(False)
            self.actionRectangular_Cursor.setChecked(False)
            self.actionRectangular_Eraser.setChecked(False)
            # self.widget.setSelectedTool(Tools.PointerCursor)
        else:
            self.actionPointer_Cursor.setChecked(True)

    @pyqtSlot()
    def on_actionRectangular_Cursor_triggered(self):
        if self.actionRectangular_Cursor.isChecked():
            self.actionPointer_Cursor.setChecked(False)
            self.actionZoom_Cursor.setChecked(False)
            self.actionRectangular_Eraser.setChecked(False)
            # self.widget.setSelectedTool(Tools.RectangularCursor)
        else:
            self.actionRectangular_Cursor.setChecked(True)

    @pyqtSlot()
    def on_actionRectangular_Eraser_triggered(self):
        if self.actionRectangular_Eraser.isChecked():
            self.actionZoom_Cursor.setChecked(False)
            self.actionPointer_Cursor.setChecked(False)
            self.actionRectangular_Cursor.setChecked(False)
            # self.widget.setSelectedTool(Tools.RectangularEraser)
        else:
            self.actionRectangular_Eraser.setChecked(True)

    #endregion

    #region Threshold

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

    def getParameters(self):
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

    def updateThreshold(self, line):
        self.detectionSettings["Threshold"] = self.toDB() if line.value() == 0 else self.toDB(line.value())

    def updateThresholdLine(self):
        self.widget.axesOscilogram.threshold.setValue(round(
            (10.0 ** ((60 + self.detectionSettings["Threshold"]) / 20.0)) * (
                2 ** self.widget.signalProcessor.signal.bitDepth) / 1000.0, 0)
                                                      * self.widget.envelopeFactor - 2 ** (
            self.widget.signalProcessor.signal.bitDepth - 1))

    def toDB(self, value=None):
        if value is None:
            return -60
        return -60 + int(20 * log10(abs(
            (value + 2 ** (self.widget.signalProcessor.signal.bitDepth - 1)) / self.widget.envelopeFactor) * 1000.0 / (
                                        2 ** self.widget.signalProcessor.signal.bitDepth)))

    @pyqtSlot(bool)
    def setVisibleThreshold(self, bool):
        self.widget.axesOscilogram.setVisibleThreshold(bool)
        self.widget.setEnvelopeVisibility(bool)

    #endregion

    #region Theme

    def load_Theme(self, theme):
        """
        Method that loads the theme to update visual options from main window.
        :param theme:
        """
        self.theme = theme
        self.widget.load_Theme(theme)

        self.widget.histogram.item.region.lineMoved()
        self.widget.histogram.item.region.lineMoveFinished()

    #endregion

    #region Visual Elements
    #The visual elements are the objects that display information about detected
    #segments. Those elements are visible on the graphs (Oscilogram and spectrogram)
    #They are divided by its definitions and purposes and user can change visibility
    #of a subset of them
    @pyqtSlot()
    def on_actionView_Parameters_triggered(self):
        """
        Changes the visibility on the window of the parameter table.
        The parameter table is where the detected segments and its measured parameters
        are displayed.
        """
        self.dockWidgetParameterTableOscilogram.setVisible(self.actionView_Parameters.isChecked())

    @pyqtSlot()
    def on_actionElements_Peaks_triggered(self):
        visibility = self.actionElements_Peaks.isChecked()
        self.widget.changeElementsVisibility(visibility, Element.PeakFreqs, oscilogramItems=False)

    @pyqtSlot()
    def on_actionTemporal_Elements_triggered(self):
        """
        Temporal Elements are the elements that are visible on the oscilogram graph.
        This method allows to change its visibility
        """
        visibility = self.actionTemporal_Elements.isChecked()
        for e in self.widget.Elements:
            e.visible = visibility
        self.widget.drawElements(oscilogramItems=True)

        self.actionTemporal_Figures.setEnabled(visibility)
        self.actionTemporal_Numbers.setEnabled(visibility)

    @pyqtSlot()
    def on_actionTemporal_Numbers_triggered(self):
        """
        Change visibility of the numbers of the detected segments on the oscilogram graph

        """
        visibility = self.actionTemporal_Numbers.isChecked()
        self.widget.changeElementsVisibility(visibility, Element.Text)

    @pyqtSlot()
    def on_actionSpectral_Numbers_triggered(self):
        """
        Change visibility of the numbers of the detected segments on the spectrogram graph
        """
        visibility = self.actionSpectral_Numbers.isChecked()
        self.widget.changeElementsVisibility(visibility, Element.Text, oscilogramItems=False)

    @pyqtSlot()
    def on_actionSpectral_Figures_triggered(self):
        """
        Change visibility of the figures of the detected segments on the spectrogram graph
        """
        visibility = self.actionSpectral_Figures.isChecked()
        self.widget.changeElementsVisibility(visibility, Element.Figures, oscilogramItems=False)

    @pyqtSlot()
    def on_actionTemporal_Figures_triggered(self):
        """
        Change visibility of the figures of the detected segments on the oscilogram graph
        """
        visibility = self.actionTemporal_Figures.isChecked()
        self.widget.changeElementsVisibility(visibility, Element.Figures, oscilogramItems=True)

    @pyqtSlot()
    def on_actionSpectral_Elements_triggered(self):
        """
        Spectral Elements are the elements that are visible on the spectrogram graph.
        This method allows to change its visibility
        """
        visibility = self.actionSpectral_Elements.isChecked()
        for e in self.widget.Elements:
            for e2 in e.twoDimensionalElements:
                e2.visible = visibility
        self.widget.drawElements(oscilogramItems=False)
        self.actionSpectral_Figures.setEnabled(visibility)
        self.actionSpectral_Numbers.setEnabled(visibility)
        self.actionSub_Elements_Peaks.setEnabled(visibility)


    #endregion

    #region Graphs Images
    #Methods taht allows to save images from a gui widget
    #use a screenshot of the control. This mean that the control has to be visible
    #for take a picture of it.
    @pyqtSlot()
    def on_actionOsgram_Image_triggered(self):
        """
        Save the Oscilogram widget graph as image
        """
        if self.widget.visibleOscilogram:
            self.saveImage(self.widget.axesOscilogram, self.tr(u"oscilogram"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The Oscilogram plot widget is not visible.") + u" \n" + self.tr(
                                          u"You should see the data that you are going to save."))

    @pyqtSlot()
    def on_actionCombined_Image_triggered(self):
        """
        Save as one image the two controls that visualize the signal
        Oscilogram and Spectrogram.
        """
        if self.widget.visibleOscilogram and self.widget.visibleSpectrogram:
            self.saveImage(self.widget, self.tr(u"graph"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"One of the plot widgets is not visible") + u" \n" + self.tr(
                                          u"You should see the data that you are going to save."))


    @pyqtSlot()
    def on_actionSpecgram_Image_triggered(self):
        """
        Save the Spectrogram widget graph as image
        """
        if self.widget.visibleSpectrogram:
            self.saveImage(self.widget.axesSpecgram, self.tr(u"specgram"))
        else:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The Espectrogram plot widget is not visible.") + u" \n" + self.tr(
                                          u"You should see the data that you are going to save."))


    def saveImage(self, widget, text=""):
        """
        Method that saves as image a widget by taking a screenshot of it.
        All the signal graphs save images methods delegate in this one their
        implementation.
        :param widget: The widget to save the screenshot.
        :param text: Alternative image name to specify the widget or graph source of the picture.
        """
        fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save") + u" " + text + self.tr(u" as an Image "),
                                                    str(self.widget.signalName()) + u"-" + text + self.tr(
                                                        u"-Duetto-Image"), "*.jpg"))
        if fname:
            #save as image
            image = QtGui.QPixmap.grabWindow(widget.winId())
            image.save(fname, 'jpg')

    #endregion

    #region Save Meditions, Excell and Batch Process
    # After detection&classification of segments and parameters measurement
    #user can save its meditions as excell or other formats
    #
    @pyqtSlot()
    def on_actionMeditions_triggered(self, name="", table=None):
        """
        Save
        :param name:
        :param table:
        :return:
        """
        if name != "":
            fname = name
        else:
            if not self.widget.signalProcessor.signal.opened():
                return
            fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save meditions as excel file"),
                                                        self.widget.signalName() + ".xls", "*.xls"))
        if fname:
            wb = xlwt.Workbook()
            a = unicode(self.tr(u"Elements Meditions"))
            ws = wb.add_sheet(a)
            self.writedata(ws, table)
            #add spectral meditions
            wb.save(fname)

    @pyqtSlot()
    def startBatchProcess(self):
        """
        Start a batch processing of signals with the configured parameters
        User must configure the settings for detection&classification and parameter
        measurement, select a folder of imput audio files and a folder for the output meditions.
        """
        thread = QtCore.QThread(self)
        #implementation of batch on a diferent thread to
        #keep user interaction responsive.
        class worker(QtCore.QObject):
            def __init__(self, worker):
                QtCore.QObject.__init__(self)
                self.work = worker

        processworker = worker(self.batch)
        thread.started.connect(processworker.work)
        processworker.moveToThread(thread)
        thread.start()

    def getSpectralData(self, signal, specgramSettings):
        """
        returns the spectral data pxx,bins and freqs of spectrogram
        """
        overlap = int(specgramSettings.NFFT * specgramSettings.overlap / 100)
        return mlab.specgram(signal.data, specgramSettings.NFFT, Fs=signal.samplingRate,
                             detrend=mlab.detrend_none, window=specgramSettings.window, noverlap=overlap,
                             sides="onesided")

    def batch(self):
        """
        Method that performs the batch procesing
        :return:
        """
        #get the input audio files folder
        #and the output meditions folder
        directoryinput = str(self.lineeditFilePath.text())
        directoryoutput = str(self.lineEditOutputFolder.text())

        #validate the folders
        if not os.path.isdir(directoryinput):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The input path is not a directory."))
            return
        if not os.path.isdir(directoryoutput):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The output path is not a directory."))
            return

        sounds = []  #the audio files tgo process
        raiz = ""

        #listing all files in directoryinput folder
        for root, dirs, files in os.walk(directoryinput):
            raiz = root if raiz == "" else raiz
            for f in files:
                #get all the files to process
                sounds.append(os.path.join(root, f))

        #updating the progress bar
        self.progressBarProcesed.setValue(0)

        # the number of files processed for use in the progres bar update
        files_processed = 0
        if self.rbttnDetection.isChecked():
            detector = OneDimensionalElementsDetector()

            #if the meditions has to export as single file
            singlefile = self.cbxSingleFile.isChecked()

            if singlefile:
                wb = xlwt.Workbook()

            for filename in sounds:
                try:
                    #process every file
                    signalProcessor = SignalProcessor()
                    signalProcessor.signal = WavFileSignal(filename)
                    #send a message for the user
                    self.listwidgetProgress.addItem(self.tr(u"Processing") + u" " + signalProcessor.signal.name)

                    table = QtGui.QTableWidget()
                    spSettngs = SpecgramSettings(self.widget.specgramSettings.NFFT,
                                                 self.widget.specgramSettings.overlap,
                                                 self.widget.specgramSettings.window)

                    #get the detection parameters
                    spSettngs.Pxx, spSettngs.freqs, spSettngs.bins = self.getSpectralData(signalProcessor.signal,
                                                                                          self.widget.specgramSettings)

                    #detect
                    detector.detect(signalProcessor.signal, 0, len(signalProcessor.signal.data),
                                    threshold=abs(self.detectionSettings["Threshold"]),
                                    decay=self.detectionSettings["Decay"], minSize=self.detectionSettings["MinSize"],
                                    softfactor=self.detectionSettings["SoftFactor"],
                                    merge_factor=self.detectionSettings["MergeFactor"],
                                    secondThreshold=abs(self.detectionSettings["Threshold2"]),
                                    specgramSettings=spSettngs,
                                    detectionsettings=self.algorithmDetectorSettings,
                                    threshold_spectral=self.detectionSettings["ThresholdSpectral"],
                                    minsize_spectral=(self.detectionSettings["minSizeFreqSpectral"],
                                                      self.detectionSettings["minSizeTimeSpectral"]),
                                    location=self.spectralMeasurementLocation,
                                    findSpectralSublements=False)

                    #get parameters to measure
                    paramsTomeasure = self.getParameters()
                    table.setRowCount(detector.elementCount())

                    #get the clasification data
                    validcategories = [k for k in self.classificationData.categories.keys() if
                                       len(self.classificationData.getvalues(k)) > 0]
                    self.elementsClasificationTableData = [[[k, self.tr(u"No Identified")] for k in validcategories] for
                                                           _ in range(table.rowCount())]

                    table.setColumnCount(len(paramsTomeasure) + len(validcategories))
                    self.columnNames = [label[0] for label in paramsTomeasure]

                    #set the name of columns
                    table.setHorizontalHeaderLabels(self.columnNames + validcategories)
                    table.resizeColumnsToContents()

                    self.listwidgetProgress.addItem(self.tr(u"Save data of ") + signalProcessor.signal.name)

                    #measure parameters
                    for i, element in enumerate(detector.elements):
                        for j, prop in enumerate(paramsTomeasure):
                            dictionary = dict(prop[2] if prop[2] is not None else [])
                            #save the meditions into the table field
                            item = QtGui.QTableWidgetItem(str(prop[1](element, dictionary)))
                            item.setBackgroundColor(
                                self.parameterTable_rowcolor_odd if i % 2 == 0 else self.parameterTable_rowcolor_even)
                            table.setItem(i, j, item)

                        for c in range(len(validcategories)):
                            try:
                                val = self.elementsClasificationTableData[i][c][1]
                                item = QtGui.QTableWidgetItem(unicode(val))
                                item.setBackgroundColor(
                                    self.parameterTable_rowcolor_odd if i % 2 == 0 else self.parameterTable_rowcolor_even)
                            except Exception as e:
                                item = QtGui.QTableWidgetItem(0)  #"Error"+e.message)
                            table.setItem(i, c + len(paramsTomeasure), item)

                    if singlefile:
                        #save meditions as new sheet in same file
                        ws = wb.add_sheet(signalProcessor.signal.name)
                        self.writedata(ws, table)
                    else:
                        #save meditions as new file
                        self.on_actionMeditions_triggered(
                            os.path.join(directoryoutput, signalProcessor.signal.name + ".xls"), table)

                    #update progress
                    self.listwidgetProgress.addItem(signalProcessor.signal.name + u" " + self.tr(u"has been files_processed"))
                    self.listwidgetProgress.update()
                    files_processed += 1
                except Exception as e:
                    self.listwidgetProgress.addItem(self.tr(u"Some problem found while processing") + u" " + e.message)
                self.progressBarProcesed.setValue(round(100.0 * (files_processed) / len(sounds)))
                self.progressBarProcesed.update()

                if singlefile:
                    wb.save(os.path.join(directoryoutput, self.tr(u"Duetto Sound Lab Meditions") + u".xls"))
                    #TODO open file after save

        if self.rbttnSplitFile.isChecked():
            save = WavFileSignal()
            for filename in sounds:
                try:
                    signal = WavFileSignal(filename)
                    self.listwidgetProgress.addItem(self.tr(u"Processing") + u" " + signal.name)
                    save.channels = signal.channels
                    save.bitDepth = signal.bitDepth
                    save.samplingRate = signal.samplingRate
                    sr = signal.samplingRate
                    pieceSize = self.spboxSplitTime.value() * sr
                    pieces = len(signal.data) / pieceSize
                    left = len(signal.data) % pieceSize
                    if (pieces >= 1):
                        for i in range(pieces):
                            save.data = signal.data[i * pieceSize:(i + 1) * pieceSize]
                            save.save(os.path.join(directoryoutput, str(i + 1) + "-" + signal.name))
                    if left > 0:
                        save.data = signal.data[len(signal.data) - left:]
                        save.save(os.path.join(directoryoutput, str(pieces + 1) + "-" + signal.name))
                    files_processed += 1
                    self.progressBarProcesed.setValue(100.0 * files_processed / len(sounds))
                    self.listwidgetProgress.addItem(signal.name + u" " + self.tr(u"has been files_processed"))
                    self.progressBarProcesed.update()
                    self.listwidgetProgress.update()
                except:
                    print(self.tr(u"some split problems"))
        self.progressBarProcesed.setValue(100)

    def selectInputFolder(self):
        inputfolder = QFileDialog.getExistingDirectory()
        self.lineeditFilePath.setText(inputfolder)

    def selectOutputFolder(self):
        outputfolder = QFileDialog.getExistingDirectory()
        self.lineEditOutputFolder.setText(outputfolder)

    def writedata(self, ws, tableParameter=None):
        """
        write the data from the table into an excell file.
        :param ws:WorkSheet object from xwlt module for interacts with excell files.
        :param tableParameter: QTableWidget with the information of the data to save.
        """
        if (tableParameter is None):
            tableParameter = self.tableParameterOscilogram

        #write the data of the meditions into the stylesheet of excell ws
        styleheader = xlwt.easyxf('font: name Times New Roman, color-index black, bold on, height 300')
        stylebody = xlwt.easyxf('font: name Times New Roman, color-index black, height 220', num_format_str='#,##0.00')
        stylecopyrigth = xlwt.easyxf('font: name Arial, color-index pale_blue, height 250, italic on',
                                     num_format_str='#,##0.00')
        #set headers
        headers = [str(tableParameter.takeHorizontalHeaderItem(pos).text()) for pos in
                   range(tableParameter.columnCount())]

        for index, header in enumerate(headers):
            ws.write(0, index, header, styleheader)

        for i in range(1, tableParameter.model().rowCount() + 1):
            for j in range(tableParameter.model().columnCount()):
                if tableParameter.item(i - 1, j):
                    ws.write(i, j, str(tableParameter.item(i - 1, j).data(Qt.DisplayRole).toString()), stylebody)
                else:
                    ws.write(i, j, unicode(self.tr(u"No Identified")), stylebody)
        #write data
        #ws object must be part of a Woorkbook that would be saved later
        ws.write(tableParameter.model().rowCount() + 3, 0, unicode(self.tr(u"Duetto Sound Lab Oscilogram Meditions")),
                 stylecopyrigth)

    #endregion

    #region Detection

    def getSettings(self, elementsDetectorDialog):
        """
        get the detection settings
        :param elementsDetectorDialog: dialog that contains the parameter tree with all the options
        :return:
        """
        self.detectionSettings["Threshold"] = self.ParamTree.param(
            unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Threshold (db)'))).value()
        self.detectionSettings["Threshold2"] = self.ParamTree.param(
            unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Threshold 2(db)'))).value()
        self.detectionSettings["MinSize"] = self.ParamTree.param(
            unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Min Size (ms)'))).value()
        self.detectionSettings["MergeFactor"] = self.ParamTree.param(
            unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Merge Factor (%)'))).value()
        self.detectionSettings["SoftFactor"] = self.ParamTree.param(
            unicode(self.tr(u'Temporal Detection Settings'))).param(unicode(self.tr(u'Soft Factor'))).value()
        self.detectionSettings["Decay"] = self.ParamTree.param(unicode(self.tr(u'Temporal Detection Settings'))).param(
            unicode(self.tr(u'Decay (ms)'))).value()
        self.algorithmDetectorSettings = elementsDetectorDialog.detectionSettings

        #spectral
        self.detectionSettings["ThresholdSpectral"] = self.ParamTree.param(
            unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Threshold (%)'))).value()
        self.detectionSettings["minSizeFreqSpectral"] = self.ParamTree.param(
            unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Minimum size'))).param(
            unicode(self.tr(u'Frequency (kHz)'))).value()
        self.detectionSettings["minSizeTimeSpectral"] = self.ParamTree.param(
            unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Minimum size'))).param(
            unicode(self.tr(u'Time (ms)'))).value()
        self.updateThresholdLine()
        #parameters

        for name, dict in self.meditions:
            for x in dict:
                if isinstance(x[1], bool):
                    x[1] = self.ParamTree.param(name).param(x[0]).value()
                else:
                    for y in x[1]:
                        y[1] = self.ParamTree.param(name).param(x[0]).param(y[0]).value()
                    for y in x[2]:
                        y[1] = self.ParamTree.param(name).param(x[0]).param(y[0]).value()

        #measurements u'Measurement Location'
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

    def updateDetectionProgressBar(self, x):
        """
        update the detection progress bar.
        detection progress bar provides a visible interface
        of the execution progress of consuming time actions such detection and classification.

        :param x: Value to set in the progress bar
        """
        self.windowProgressDetection.setValue(x)

    def elementSelectedInTable(self, row, column=0):
        """
        Callback that is executed for update the element that is selected.
        An element is selected by the user ad must be updated in all visible representations
        like table parameter, twodimensional windows, and graphs.
        :param row: index of the element selected
        :param column: parameter provided to reuse this method as callabck of the event selected cell
        in the QTableWidget
        """
        self.tableParameterOscilogram.selectRow(row)
        self.widget.selectElement(row)  #select the correct element in oscilogram
        for wnd in self.twodimensionalGraphs:
            wnd.selectElement(row)

    @pyqtSlot()
    def on_actionDetection_triggered(self):
        """
        Method that execute the detection

        """
        #TODO check if is possible to merge the code in this method and the batch.
        #TODO common factor code

        elementsDetectorDialog = ElemDetectSettingsDialog(parent=self, paramTree=self.ParamTree)
        elementsDetectorDialog.load_Theme(self.theme)
        self.widget.selectElement(-1)
        try:
            if elementsDetectorDialog.exec_():
                try:

                    self.getSettings(elementsDetectorDialog)

                    self.actionView_Threshold.setChecked(True)
                    paramsTomeasure = self.getParameters()
                    self.windowProgressDetection.resize(self.widget.width() / 3,
                                                        self.windowProgressDetection.size().height())
                    self.windowProgressDetection.move(self.widget.x() + self.widget.width() / 3,
                                                      self.widget.y() - self.windowProgressDetection.height() / 2 + self.widget.height() / 2)
                    self.windowProgressDetection.show()
                    self.widget.detectElements(threshold=abs(self.detectionSettings["Threshold"]),
                                               detectionsettings=self.algorithmDetectorSettings,
                                               decay=self.detectionSettings["Decay"],
                                               minSize=self.detectionSettings["MinSize"],
                                               softfactor=self.detectionSettings["SoftFactor"],
                                               merge_factor=self.detectionSettings["MergeFactor"],
                                               threshold2=abs(self.detectionSettings["Threshold2"]),
                                               threshold_spectral=self.detectionSettings["ThresholdSpectral"],
                                               minsize_spectral=(self.detectionSettings["minSizeFreqSpectral"],
                                                                 self.detectionSettings["minSizeTimeSpectral"]),
                                               location=self.spectralMeasurementLocation,
                                               progress=self.updateDetectionProgressBar,
                                               findSpectralSublements=self.ParamTree.param(
                                                   unicode(self.tr(u'Spectral Detection Settings'))).param(
                                                   unicode(self.tr(u'Detect Spectral Subelements'))).value())

                    self.tableParameterOscilogram.clear()
                    self.tableParameterOscilogram.cellPressed.connect(self.elementSelectedInTable)
                    self.tableParameterOscilogram.setRowCount(len(self.widget.Elements))
                    self.columnNames = [label[0] for label in paramsTomeasure]

                    validcategories = [k for k in self.classificationData.categories.keys() if
                                       len(self.classificationData.getvalues(k)) > 0]
                    self.elementsClasificationTableData = [[[k, self.tr(u"No Identified")] for k in validcategories] for
                                                           _ in range(self.tableParameterOscilogram.rowCount())]

                    self.tableParameterOscilogram.setColumnCount(len(paramsTomeasure) + len(validcategories))
                    self.tableParameterOscilogram.setHorizontalHeaderLabels(self.columnNames + validcategories)
                    self.updateDetectionProgressBar(95)
                    self.tableParameterOscilogram.resizeColumnsToContents()

                    #for select the element in the table. Binding for the element click to the table
                    for index in range(len(self.widget.Elements)):
                        self.widget.Elements[index].elementClicked.connect(self.elementSelectedInTable)

                    #the table of parameters stored as a numpy array
                    self.measuredParameters = np.zeros(len(self.widget.Elements) * len(paramsTomeasure)).reshape(
                        (len(self.widget.Elements), len(paramsTomeasure)))

                    for i in range(self.tableParameterOscilogram.rowCount()):
                        for j, prop in enumerate(paramsTomeasure):
                            try:
                                dictionary = dict(prop[2] if prop[2] is not None else [])
                                self.measuredParameters[i, j] = prop[1](self.widget.Elements[i], dictionary)
                                item = QtGui.QTableWidgetItem(unicode(self.measuredParameters[i, j]))
                                item.setBackgroundColor(
                                    self.parameterTable_rowcolor_odd if i % 2 == 0 else self.parameterTable_rowcolor_even)
                            except Exception as e:
                                item = QtGui.QTableWidgetItem(0)  #"Error"+e.message)

                            self.tableParameterOscilogram.setItem(i, j, item)
                        for c in range(len(validcategories)):
                            try:
                                val = self.elementsClasificationTableData[i][c][1]
                                item = QtGui.QTableWidgetItem(unicode(val))
                                item.setBackgroundColor(
                                    self.parameterTable_rowcolor_odd if i % 2 == 0 else self.parameterTable_rowcolor_even)
                            except Exception as e:
                                item = QtGui.QTableWidgetItem(0)  #"Error"+e.message)
                            self.tableParameterOscilogram.setItem(i, c + len(paramsTomeasure), item)

                    self.updateDetectionProgressBar(100)

                    for wnd in self.twodimensionalGraphs:
                        wnd.loadData(self.columnNames, self.measuredParameters)

                except Exception as e:
                    print("some detection errors" + e.message)

                self.widget.refresh()

                self.windowProgressDetection.hide()
        except:
            pass

    #endregion

    #region Classification
    @pyqtSlot()
    def on_actionClassification_Settings_triggered(self):
        """
        Open the classsification dialog for update the categories and values
        in which could be classified a segment.

        """
        editCategDialog = editCateg.Ui_Dialog()
        editCategDialogWindow = EditCategoriesDialog(self)
        editCategDialog.setupUi(editCategDialogWindow)
        widget = QWidget()
        self.clasiffCategories_vlayout = QtGui.QVBoxLayout()

        for k in self.classificationData.categories.keys():
            a = EditCategoriesWidget(self, k, self.classificationData)
            self.clasiffCategories_vlayout.addWidget(a)

        editCategDialog.bttnAddCategory.clicked.connect(self.addCategory)
        widget.setLayout(self.clasiffCategories_vlayout)
        editCategDialog.listWidget.setWidget(widget)
        editCategDialogWindow.exec_()

    def addCategory(self):
        dialog = QtGui.QDialog(self)
        dialog.setWindowTitle(self.tr(u"Create New Category"))
        layout = QtGui.QVBoxLayout()
        layout.addWidget(QtGui.QLabel(self.tr(u"Insert the name of the new Category")))
        text = QtGui.QLineEdit()
        layout.addWidget(text)
        butts = QtGui.QDialogButtonBox()

        butts.addButton(QtGui.QDialogButtonBox.Ok)
        butts.addButton(QtGui.QDialogButtonBox.Cancel)
        QtCore.QObject.connect(butts, QtCore.SIGNAL("accepted()"), dialog.accept)
        QtCore.QObject.connect(butts, QtCore.SIGNAL("rejected()"), dialog.reject)

        layout.addWidget(butts)
        dialog.setLayout(layout)
        if dialog.exec_():
            category = str(text.text())
            if category == "":
                QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"), self.tr(u"Invalid Category Name."))
                return
            if self.clasiffCategories_vlayout and self.classificationData.addCategory(category):
                self.clasiffCategories_vlayout.addWidget(EditCategoriesWidget(self, category, self.classificationData))

    def classificationCategoryValueAdded(self, category, value):
        # print("In Category "+category+" was added the value: "+value)
        pass

    def classificationCategoryValueRemove(self, category, value):
        # print("In Category "+category+" was removed the value: " + value)
        for i, elem in enumerate(self.elementsClasificationTableData):
            for j, l in enumerate(elem):
                if l[0] == category and l[1] == value:
                    self.elementsClasificationTableData[i][j][1] = self.tr(u"No Identified")
                    item = QtGui.QTableWidgetItem(unicode(self.elementsClasificationTableData[i][j][1]))
                    item.setBackgroundColor(
                        self.parameterTable_rowcolor_odd if i % 2 == 0 else self.parameterTable_rowcolor_even)
                    self.tableParameterOscilogram.setItem(i, len(self.measuredParameters[i]) + j, item)

        self.tableParameterOscilogram.update()

    def classificationCategoryAdded(self, category):
        for i, elem in enumerate(self.elementsClasificationTableData):
            self.elementsClasificationTableData[i].append([str(category), self.tr(u"No Identified")])
        print(self.elementsClasificationTableData)
        if self.tableParameterOscilogram.rowCount() > 0:
            self.tableParameterOscilogram.insertColumn(self.tableParameterOscilogram.columnCount())
            column = self.tableParameterOscilogram.columnCount() - 1
            #put rows in table
            for row in range(self.tableParameterOscilogram.rowCount()):
                item = QtGui.QTableWidgetItem(unicode(self.tr(u"No Identified")))
                item.setBackgroundColor(
                    self.parameterTable_rowcolor_odd if row % 2 == 0 else self.parameterTable_rowcolor_even)
                self.tableParameterOscilogram.setItem(row, column, item)
                self.tableParameterOscilogram.setHorizontalHeaderItem(column, QtGui.QTableWidgetItem(category))
            #insert data in clasification Data
            self.tableParameterOscilogram.update()

    def elementsClasification(self, indexes_list, dictionary):
        for i in indexes_list:
            for column, l in enumerate(self.elementsClasificationTableData[i]):
                if l[0] in dictionary:
                    self.elementsClasificationTableData[i][column][1] = dictionary[l[0]]
                    item = QtGui.QTableWidgetItem(unicode(self.elementsClasificationTableData[i][column][1]))
                    item.setBackgroundColor(
                        self.parameterTable_rowcolor_odd if i % 2 == 0 else self.parameterTable_rowcolor_even)
                    self.tableParameterOscilogram.setItem(i, len(self.measuredParameters[i]) + column, item)

        self.tableParameterOscilogram.update()

    #endregion

    #region Zoom

    @QtCore.pyqtSlot()
    def on_actionZoomIn_triggered(self):
        self.widget.zoomIn()

    @QtCore.pyqtSlot()
    def on_actionZoom_out_triggered(self):
        self.widget.zoomOut()

    @QtCore.pyqtSlot()
    def on_actionZoom_out_entire_file_triggered(self):
        self.widget.zoomNone()

    #endregion

    #region Close and Exit
    @pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()


    def closeEvent(self, event):
        if self.widget.signalProcessor.signal.playStatus == AudioSignal.PLAYING or \
                        self.widget.signalProcessor.signal.playStatus == AudioSignal.RECORDING:
            self.widget.stop()
        mbox = QtGui.QMessageBox(QtGui.QMessageBox.Question, self.tr(u"Save meditions"),
                                 self.tr(u"Do you want to save the meditions?"),
                                 QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, self)
        if self.tableParameterOscilogram.rowCount() > 0:
            result = mbox.exec_()
            if result == QtGui.QMessageBox.Cancel:
                event.ignore()
                return
            elif result == QtGui.QMessageBox.Yes:
                wb = xlwt.Workbook()
                ws = wb.add_sheet(self.widget.signalName())
                self.writedata(ws, self.tableParameterOscilogram)
                fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save meditions as excel file"),
                                                            self.widget.signalName() + ".xls", "*.xls"))
                if fname:
                    wb.save(fname)
            for w in self.twodimensionalGraphs:
                w.close()

    #endregion

    #region Time and Frecuency Domain Visualization
    @pyqtSlot()
    def on_actionClear_Meditions_triggered(self):
        self.widget.clearDetection()
        self.widget.selectElement()
        self.widget.visualChanges = True
        self.widget.refresh()

    @QtCore.pyqtSlot()
    def on_actionCombined_triggered(self):
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = True
        self.widget.refresh(dataChanged=False)


    @QtCore.pyqtSlot()
    def on_actionSpectogram_triggered(self):
        self.widget.visibleOscilogram = False
        self.widget.visibleSpectrogram = True
        self.widget.refresh(dataChanged=False)


    @QtCore.pyqtSlot()
    def on_actionOscilogram_triggered(self):
        self.widget.visibleOscilogram = True
        self.widget.visibleSpectrogram = False
        self.widget.refresh(dataChanged=False)

    #endregion

    #region Sound
    @QtCore.pyqtSlot()
    def on_actionPlay_Sound_triggered(self):
        self.widget.play()

    @QtCore.pyqtSlot()
    def on_actionStop_Sound_triggered(self):
        self.widget.stop()

    @QtCore.pyqtSlot()
    def on_actionPause_Sound_triggered(self):
        self.widget.pause()

    #endregion

    @pyqtSlot()
    def on_actionDelete_Selected_Elements_triggered(self):
        indx = self.widget.deleteSelectedElements

        if indx is not None and indx[0] >= 0 and indx[1] < self.tableParameterOscilogram.rowCount():
            for i in range(indx[1], indx[0] - 1, -1):
                #delete from table
                self.tableParameterOscilogram.removeRow(i)

            for i in range(self.tableParameterOscilogram.rowCount()):
                #update table bacground color
                for j in range(self.tableParameterOscilogram.columnCount()):
                    self.tableParameterOscilogram.item(i, j).setBackgroundColor(
                        self.parameterTable_rowcolor_odd if i % 2 == 0 else self.parameterTable_rowcolor_even)

            #updates the numpy array  with the detected parameters
            self.measuredParameters = np.concatenate(
                (self.measuredParameters[:indx[0]], self.measuredParameters[indx[1] + 1:]))
            self.elementsClasificationTableData = self.elementsClasificationTableData[
                                                  :indx[0]] + self.elementsClasificationTableData[indx[1] + 1:]
            self.tableParameterOscilogram.update()
            for wnd in self.twodimensionalGraphs:
                wnd.loadData(self.columnNames, self.measuredParameters)

        self.on_actionDeselect_Elements_triggered()

    @pyqtSlot()
    def on_actionDeselect_Elements_triggered(self):
        self.widget.selectElement()  # select the element
        self.widget.clearZoomCursor()

        for wnd in self.twodimensionalGraphs:
            wnd.deselectElement()

