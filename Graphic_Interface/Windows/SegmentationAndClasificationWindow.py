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
from Utils.Utils import saveImage
from graphic_interface.widgets.signal_visualizer_tools.SignalVisualizerTool import Tools
from sound_lab_core.Clasification.ClassificationData import ClassificationData
from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    DetectionType, AutomaticThresholdType, DetectionSettings
from sound_lab_core.Segmentation.Detectors.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector
from sound_lab_core.Segmentation.Elements.Element import Element
from sound_lab_core.Segmentation.Elements.OneDimensionalElement import SpectralMeasurementLocation
from ..dialogs.elemDetectSettings import ElemDetectSettingsDialog
from graphic_interface.windows.TwoDimensionalAnalisysWindow import TwoDimensionalAnalisysWindow
from graphic_interface.windows.ui_python_files.SegmentationAndClasificationWindowUI import Ui_MainWindow
import graphic_interface.windows.ui_python_files.EditCategoriesDialogUI as editCateg
from graphic_interface.dialogs.EditCategoriesDialog import EditCategoriesDialog
from graphic_interface.widgets.EditCategoriesWidget import EditCategoriesWidget
from SoundLabWindow import SoundLabWindow


class SegmentationAndClasificationWindow(SoundLabWindow, Ui_MainWindow):
    """
    Window that process the segmentation and classification of a signal
    Contains a QSignalDetectorWidget that wrapper several functionalities
    Allows to select the segmentations and clasifications settings,
    and parameter measurement for detected segments.
    Provides a table for visualization of segment and measures,
    A two dimensional window to graph two measured params. One for each axis.
    Options for selection and visualization of segments
    Provides options for save the meditions to excell.
    """

    # CONSTANTS
    # different colors for the even and odds rows in the parameter table and segment colors.
    TABLE_ROW_COLOR_ODD = QtGui.QColor(0, 0, 255, 150)
    TABLE_ROW_COLOR_EVEN = QtGui.QColor(0, 255, 0, 150)

    # region Initialize

    def __init__(self, parent, signal):
        """
        Create a the window of segmentation and clasiffication.
        :param parent: the parent widget if any
        :param signal: the signal to visualize for segmentation and clasiffication
        :return:
        """
        # set the visual variables and methods from ancesters
        SoundLabWindow.__init__(self, parent)
        self.setupUi(self)


        # check the parameters
        if signal is None or not isinstance(signal, AudioSignal):
            raise Exception("The signal to analyze must be of type AudioSignal")

        # set the signal to the widget
        self.widget.signal = signal
        self.widget.graph()

        # set visible the two widgets by default
        self.changeWidgetsVisibility(True, True)

        # connect the signal of the widget for new detected data by its tools
        self.widget.toolDataDetected.connect(self.updateStatusBar)

        self.dockWidgetParameterTableOscilogram.setVisible(False)
        self.tableParameterOscilogram.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.show()

        self.algorithmDetectorSettings = DetectionSettings(DetectionType.Envelope_Abs_Decay_Averaged,
                                                           AutomaticThresholdType.Global_MaxMean)

        self.spectralMeasurementLocation = SpectralMeasurementLocation()

        # self.widget.axesOscilogram.threshold.sigPositionChangeFinished.connect(self.updateThreshold)
        # self.widget.axesOscilogram.threshold.setBounds((-2 ** (self.widget.signal.bitDepth - 1),
        #                                                 2 ** (self.widget.signal.bitDepth - 1)))

        self.detectionSettings = {"Threshold": -40, "Threshold2": 0, "MergeFactor": 5, "MinSize": 1, "Decay": 1,
                                  "SoftFactor": 6, "ThresholdSpectral": 95, "minSizeTimeSpectral": 0,
                                  "minSizeFreqSpectral": 0}

        # for select the element in the table. Binding for the element click to the table
        self.widget.elementClicked.connect(self.elementSelectedInTable)

        # region Detection Params Definition

        # Time And Spectral Medition Parameters
        # the medition parameters are defined here
        # are divided into time and spectral meditions
        # time are those parameters that are measured in time domain. ie Oscilogram
        # spectral meditions are measured on spectrogram
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

        # parameter tree to provide the measurement and parameter configuration into the dialog
        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)

        # the spectral parameters that changes in function of the location measurements
        # the order of the elements in the array of self.parameterMeasurement["Temporal"]
        # is relevant for the visualization in the table and the
        # binding to the checkboxes in the dialog of parameter measurement

        # add the context menu actions to the widget
        self.__addContextMenuActions()

        # create the progress bar that is showed while the detection is made
        self.windowProgressDetection = QtGui.QProgressBar(self.widget)

        # set the name of the signal to the visible label
        self.actionSignalName.setText(self.widget.signalName)

        # array of windows with two dimensional graphs.
        # Are stored for a similar behavior to the one dimensional
        # in the main window. Updates the windows graphs on change etc
        self.two_dim_windows = []

        # stores the measured parameters of the detected elements
        self.measuredParameters = np.array([[], []])

        # set the connections for the classification data to
        # update when is added, changed or deleted a value or category
        self.classificationData = ClassificationData()
        self.classificationData.valueAdded.connect(self.classificationCategoryValueAdded)
        self.classificationData.valueRemoved.connect(self.classificationCategoryValueRemove)
        self.classificationData.categoryAdded.connect(self.classificationCategoryAdded)

        # stores the classification data that are present in the table of meditions
        # has the form of a list with [["category name","category value"]] for each element
        # example with 2 elements and 2 categories
        # [[["Specie","Cartacuba"],["Location","Cuba"]],
        # [["Specie","Sinsonte"],["Location","Camaguey"]]]
        self.elementsClasificationTableData = []

        # the names of the columns in the table of parameters measured
        self.columnNames = []

    def __addContextMenuActions(self):
        """
        Add the context menu actions into the widget in the creation process of the window
        :return:
        """
        separator, separator1, separator2, separator3, separator4 = [QtGui.QAction(self) for _ in range(5)]

        for sep in [separator, separator1, separator2, separator3, separator4]:
            sep.setSeparator(True)

        # region Context Menu Actions

        self.widget.createContextCursor(
            [
                # Zoom Actions
                self.actionZoomIn,
                self.actionZoom_out,
                self.actionZoom_out_entire_file,
                separator1,

                # widgets visibility actions
                self.actionCombined,
                self.actionOscilogram,
                self.actionSpectogram,
                separator,

                # meditions manipulation actions
                self.actionClear_Meditions,
                self.actionMeditions,
                self.actionView_Parameters,
                separator2,

                # change tools actions
                self.actionZoom_Cursor,
                self.actionPointer_Cursor,
                self.actionRectangular_Cursor,
                self.actionRectangular_Eraser,
                separator3,

                # elements select/deselect
                self.actionDeselect_Elements,
                self.actionDelete_Selected_Elements,
                separator4,

                # widgets images
                self.actionOsgram_Image,
                self.actionSpecgram_Image,
                self.actionCombined_Image])
        # endregion

    def configureToolBarActionsGroups(self):
        """
        :return:
        """
        SoundLabWindow.configureToolBarActionsGroups(self)

    # endregion

    # region Detection

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

        # spectral
        self.detectionSettings["ThresholdSpectral"] = self.ParamTree.param(
            unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Threshold (%)'))).value()
        self.detectionSettings["minSizeFreqSpectral"] = self.ParamTree.param(
            unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Minimum size'))).param(
            unicode(self.tr(u'Frequency (kHz)'))).value()
        self.detectionSettings["minSizeTimeSpectral"] = self.ParamTree.param(
            unicode(self.tr(u'Spectral Detection Settings'))).param(unicode(self.tr(u'Minimum size'))).param(
            unicode(self.tr(u'Time (ms)'))).value()
        self.updateThresholdLine()
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
        # select the element in the table of meditions
        self.tableParameterOscilogram.selectRow(row)

        # in the widget...
        self.widget.selectElement(row)

        # and in the opened two dimensional windows
        for wnd in self.two_dim_windows:
            wnd.selectElement(row)

    @pyqtSlot()
    def on_actionDetection_triggered(self):
        """
        Method that execute the detection
        """
        # TODO check if is possible to merge the code in this method and the batch.
        # TODO common factor code
        elementsDetectorDialog = ElemDetectSettingsDialog(parent=self, paramTree=self.ParamTree, signal=self.widget.signal)
        elementsDetectorDialog.load_workspace(self.workSpace)

        # deselect the elements on the widget
        self.widget.deselectElement()
        try:
            if elementsDetectorDialog.exec_():
                self.getSettings(elementsDetectorDialog)

                self.actionView_Threshold.setChecked(True)
                paramsTomeasure = self.getParameters()

                self.__showProgressBar()

                # execute the detection
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

                # clasification data update TODO improve comments and implementation
                validcategories = [k for k in self.classificationData.categories.keys() if
                                   len(self.classificationData.getvalues(k)) > 0]

                self.elementsClasificationTableData = [[[k, self.tr(u"No Identified")] for k in validcategories] for
                                                       _ in range(self.tableParameterOscilogram.rowCount())]

                # clear the previous meditions
                self.tableParameterOscilogram.clear()

                self.tableParameterOscilogram.setRowCount(len(self.widget.Elements))

                # connect the table selection with the selection of an element
                self.tableParameterOscilogram.cellPressed.connect(self.elementSelectedInTable)

                # get the column names of the meditions and set them on the table headers
                self.columnNames = [label[0] for label in paramsTomeasure]
                self.tableParameterOscilogram.setHorizontalHeaderLabels(self.columnNames + validcategories)

                # set the number of columns to the amount of parameters measured
                # plus the amount of categories of clasiffication
                self.tableParameterOscilogram.setColumnCount(len(paramsTomeasure) + len(validcategories))
                self.updateDetectionProgressBar(95)
                self.tableParameterOscilogram.resizeColumnsToContents()

                # the table of parameters stored as a numpy array
                self.measuredParameters = np.zeros(len(self.widget.Elements) * len(paramsTomeasure)).reshape(
                    (len(self.widget.Elements), len(paramsTomeasure)))

                for i in range(self.tableParameterOscilogram.rowCount()):
                    for j, params in enumerate(paramsTomeasure):
                        try:
                            # get the function params.
                            # params[0] is the name of the param measured
                            # params[1] is the function to measure the param
                            # params[2] is the dictionary of params supplied to the function
                            dictionary = dict(params[2] if params[2] is not None else [])

                            # compute the param with the function
                            self.measuredParameters[i, j] = params[1](self.widget.Elements[i], dictionary)

                            # set the result to a table item and save it on the table
                            item = QtGui.QTableWidgetItem(unicode(self.measuredParameters[i, j]))

                            # color options for the rows of the table
                            item.setBackgroundColor(
                                self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)

                        except Exception as e:
                            # if some error is raised set a default value
                            item = QtGui.QTableWidgetItem(0)  # "Error"+e.message)

                        self.tableParameterOscilogram.setItem(i, j, item)

                    for c in range(len(validcategories)):
                        try:
                            val = self.elementsClasificationTableData[i][c][1]
                            item = QtGui.QTableWidgetItem(unicode(val))
                            item.setBackgroundColor(
                                self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)

                        except Exception as e:
                            # if some error is raised set a default value
                            item = QtGui.QTableWidgetItem(0)  # "Error"+e.message)
                        self.tableParameterOscilogram.setItem(i, c + len(paramsTomeasure), item)

                # complete the progress of detection and hide the progress bar
                self.updateDetectionProgressBar(100)
                self.windowProgressDetection.hide()

                # update the measured data on the two dimensional opened windows
                for wnd in self.two_dim_windows:
                    wnd.loadData(self.columnNames, self.measuredParameters)

            # refresh changes
            self.widget.graph()

        except Exception as e:
            print("detection errors: " + e.message)

    def __showProgressBar(self):
        """
        Show the progress bar in the middle of the widget.
        Used when a high time demanding task is going to be made to
        show to the user it's progress.
        :return:
        """
        self.windowProgressDetection.resize(self.widget.width() / 3,
                                            self.windowProgressDetection.size().height())
        self.windowProgressDetection.move(self.widget.x() + self.widget.width() / 3,
                                          self.widget.y() - self.windowProgressDetection.height() / 2 + self.widget.height() / 2)
        self.windowProgressDetection.show()

    # endregion

    # region Classification
    @pyqtSlot()
    def on_actionClassification_Settings_triggered(self):
        """
        Open the classification dialog for update the categories and values
        in which could be classified a segment.
        """
        # create and open the dialog
        editCategDialog = editCateg.Ui_Dialog()
        editCategDialogWindow = EditCategoriesDialog(self)
        editCategDialog.setupUi(editCategDialogWindow)

        self.clasiffCategories_vlayout = QtGui.QVBoxLayout()

        for k in self.classificationData.categories.keys():
            # foreach clasification category add a widget to show it
            widget = EditCategoriesWidget(self, k, self.classificationData)
            self.clasiffCategories_vlayout.addWidget(widget)

        # connect the methods for add category action
        editCategDialog.bttnAddCategory.clicked.connect(self.addCategory)

        widget = QWidget()
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
                        self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)
                    self.tableParameterOscilogram.setItem(i, len(self.measuredParameters[i]) + j, item)

        self.tableParameterOscilogram.update()

    def classificationCategoryAdded(self, category):
        for i, elem in enumerate(self.elementsClasificationTableData):
            self.elementsClasificationTableData[i].append([str(category), self.tr(u"No Identified")])

        if self.tableParameterOscilogram.rowCount() > 0:
            self.tableParameterOscilogram.insertColumn(self.tableParameterOscilogram.columnCount())
            column = self.tableParameterOscilogram.columnCount() - 1
            # put rows in table
            for row in range(self.tableParameterOscilogram.rowCount()):
                item = QtGui.QTableWidgetItem(unicode(self.tr(u"No Identified")))
                item.setBackgroundColor(
                    self.TABLE_ROW_COLOR_ODD if row % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)
                self.tableParameterOscilogram.setItem(row, column, item)
                self.tableParameterOscilogram.setHorizontalHeaderItem(column, QtGui.QTableWidgetItem(category))
            # insert data in clasification Data
            self.tableParameterOscilogram.update()

    def elementsClasification(self, indexes_list, dictionary):
        for i in indexes_list:
            for column, l in enumerate(self.elementsClasificationTableData[i]):
                if l[0] in dictionary:
                    self.elementsClasificationTableData[i][column][1] = dictionary[l[0]]
                    item = QtGui.QTableWidgetItem(unicode(self.elementsClasificationTableData[i][column][1]))
                    item.setBackgroundColor(
                        self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)
                    self.tableParameterOscilogram.setItem(i, len(self.measuredParameters[i]) + column, item)

        self.tableParameterOscilogram.update()

    # endregion

    # region Two Dimensional Graphs

    @pyqtSlot()
    def on_actionTwo_Dimensional_Graphs_triggered(self):
        """
        Creates a new two dimensional window for analysis.
        :return:
        """
        # a two dim window must be created after segment detection
        # and parameters measurement
        if self.tableParameterOscilogram.rowCount() == 0:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"There is not detected elements.") + u" \n" + self.tr(
                                          u"The two dimensional analyses requires at least one detected element."))
            return

        if self.tableParameterOscilogram.columnCount() == 0:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"There is not parameters measurement.") + u"\n" + self.tr(
                                          u"The two dimensional analisys requires at least one parameter measured."))
            return

        wnd = TwoDimensionalAnalisysWindow(self, columns=self.columnNames, data=self.measuredParameters,
                                           classificationData=self.classificationData)

        # connect the signals for update the new two dim window actions
        wnd.elementSelected.connect(self.elementSelectedInTable)
        wnd.elementsClasiffied.connect(self.elementsClasification)

        # load the theme in the new two dimensional window
        if self.theme:
            wnd.load_Theme(self.theme)

        # if any previous windows was opened then update in the new one the selected element
        if len(self.two_dim_windows) > 0:
            wnd.selectElement(self.two_dim_windows[0].previousSelectedElement)

        # add the new window to the current opened windows
        self.two_dim_windows.append(wnd)

    def clearTwoDimensionalWindows(self):
        """
        Close the two dimensional windows and clear the list of two dim windows
        :return:
        """
        # close the open windows
        for w in self.two_dim_windows:
            w.close()

        # initialize the list
        self.two_dim_windows = []

    # endregion

    # region Threshold
    # group of method that handles the visibility
    # of the trheshold in the oscilogram widget
    # 
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
                2 ** self.widget.signal.bitDepth) / 1000.0, 0)
                                                      * self.widget.envelopeFactor - 2 ** (
            self.widget.signal.bitDepth - 1))

    def toDB(self, value=None):
        if value is None:
            return -60
        return -60 + int(20 * log10(abs(
            (value + 2 ** (self.widget.signal.bitDepth - 1)) / self.widget.envelopeFactor) * 1000.0 / (
                                        2 ** self.widget.signal.bitDepth)))

    @pyqtSlot(bool)
    def setThresholdVisibility(self, bool):
        self.widget.axesOscilogram.setVisibleThreshold(bool)
        self.widget.setEnvelopeVisibility(bool)

    # endregion

    # region WorkSpace

    def load_workspace(self, workspace):
        """
        Method that loads the workspace to update visual options from main window.
        :param workspace:
        """
        self.workSpace = workspace
        self.widget.load_workspace(workspace)

    # endregion

    # region Visual Elements
    # The visual elements are the objects that display information about detected
    # segments. Those elements are visible on the graphs (Oscilogram and spectrogram)
    # They are divided by its definitions and purposes and user can change visibility
    # of a subset of them
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

    # endregion

    # region Save Meditions, Excell and Batch Process
    # After detection&classification of segments and parameters measurement
    # user can save its meditions as excell or other formats
    # 
    @pyqtSlot()
    def on_actionMeditions_triggered(self, name="", table=None):
        """
        Save to disc the measurement made by the window to the elements detected.
        :param name: The name of the file to save the data
        :param table: The table with the parameter to save into excel
        :return:
        """
        # get the file name to save the data into.
        if name != "":
            fname = name
        else:
            fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save meditions as excel file"),
                                                        self.widget.signalName() + ".xls", "*.xls"))
        # save the data of table
        if fname:
            # the excel book to save data
            wb = xlwt.Workbook()
            ws = wb.add_sheet(unicode(self.tr(u"Elements Meditions")))

            self.writedata(ws, table)
            wb.save(fname)

    @pyqtSlot()
    def startBatchProcess(self):
        """
        Start a batch processing of signals with the configured parameters
        User must configure the settings for detection&classification and parameter
        measurement, select a folder of imput audio files and a folder for the output meditions.
        """
        thread = QtCore.QThread(self)

        # implementation of batch on a diferent thread to
        # keep user interaction responsive.
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

        # TODO create a batch processing window
        # get the input audio files folder
        # and the output meditions folder
        directoryinput = str(self.lineeditFilePath.text())
        directoryoutput = str(self.lineEditOutputFolder.text())

        # validate the folders
        if not os.path.isdir(directoryinput):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The input path is not a directory."))
            return
        if not os.path.isdir(directoryoutput):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The output path is not a directory."))
            return

        sounds = []  # the audio files tgo process
        raiz = ""

        # listing all files in directoryinput folder
        # TODO change by the method of UTILS
        for root, dirs, files in os.walk(directoryinput):
            raiz = root if raiz == "" else raiz
            for f in files:
                # get all the files to process
                sounds.append(os.path.join(root, f))

        # updating the progress bar
        self.progressBarProcesed.setValue(0)

        # the number of files processed for use in the progres bar update
        files_processed = 0
        if self.rbttnDetection.isChecked():
            detector = OneDimensionalElementsDetector()

            # if the meditions has to export as single file
            singlefile = self.cbxSingleFile.isChecked()

            if singlefile:
                wb = xlwt.Workbook()

            for filename in sounds:
                try:
                    # process every file
                    signalProcessor = SignalProcessor()
                    signalProcessor.signal = WavFileSignal(filename)
                    # send a message for the user
                    self.listwidgetProgress.addItem(self.tr(u"Processing") + u" " + signalProcessor.signal.name)

                    table = QtGui.QTableWidget()
                    spSettngs = SpecgramSettings(self.widget.specgramSettings.NFFT,
                                                 self.widget.specgramSettings.overlap,
                                                 self.widget.specgramSettings.window)

                    # get the detection parameters
                    spSettngs.Pxx, spSettngs.freqs, spSettngs.bins = self.getSpectralData(signalProcessor.signal,
                                                                                          self.widget.specgramSettings)

                    # detect
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

                    # get parameters to measure
                    paramsTomeasure = self.getParameters()
                    table.setRowCount(detector.elementCount())

                    # get the clasification data
                    validcategories = [k for k in self.classificationData.categories.keys() if
                                       len(self.classificationData.getvalues(k)) > 0]
                    self.elementsClasificationTableData = [[[k, self.tr(u"No Identified")] for k in validcategories] for
                                                           _ in range(table.rowCount())]

                    table.setColumnCount(len(paramsTomeasure) + len(validcategories))
                    self.columnNames = [label[0] for label in paramsTomeasure]

                    # set the name of columns
                    table.setHorizontalHeaderLabels(self.columnNames + validcategories)
                    table.resizeColumnsToContents()

                    self.listwidgetProgress.addItem(self.tr(u"Save data of ") + signalProcessor.signal.name)

                    # measure parameters
                    for i, element in enumerate(detector.elements):
                        for j, prop in enumerate(paramsTomeasure):
                            dictionary = dict(prop[2] if prop[2] is not None else [])
                            # save the meditions into the table field
                            item = QtGui.QTableWidgetItem(str(prop[1](element, dictionary)))
                            item.setBackgroundColor(
                                self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)
                            table.setItem(i, j, item)

                        for c in range(len(validcategories)):
                            try:
                                val = self.elementsClasificationTableData[i][c][1]
                                item = QtGui.QTableWidgetItem(unicode(val))
                                item.setBackgroundColor(
                                    self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)
                            except Exception as e:
                                item = QtGui.QTableWidgetItem(0)  # "Error"+e.message)
                            table.setItem(i, c + len(paramsTomeasure), item)

                    if singlefile:
                        # save meditions as new sheet in same file
                        ws = wb.add_sheet(signalProcessor.signal.name)
                        self.writedata(ws, table)
                    else:
                        # save meditions as new file
                        self.on_actionMeditions_triggered(
                            os.path.join(directoryoutput, signalProcessor.signal.name + ".xls"), table)

                    # update progress
                    self.listwidgetProgress.addItem(signalProcessor.signal.name + u" " + self.tr(u"has been files_processed"))
                    self.listwidgetProgress.update()
                    files_processed += 1
                except Exception as e:
                    self.listwidgetProgress.addItem(self.tr(u"Some problem found while processing") + u" " + e.message)
                self.progressBarProcesed.setValue(round(100.0 * (files_processed) / len(sounds)))
                self.progressBarProcesed.update()

                if singlefile:
                    wb.save(os.path.join(directoryoutput, self.tr(u"Duetto Sound Lab Meditions") + u".xls"))
                    # TODO open file after save

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
        """
        Select a valid folder in the file system..
        :return:
        """
        inputfolder = QFileDialog.getExistingDirectory()

        # update the line edit with the name of
        self.lineeditFilePath.setText(inputfolder)

    def selectOutputFolder(self):
        """
        Select a valid folder in the file system to save the batch result data.
        :return:
        """
        output_folder = QFileDialog.getExistingDirectory()
        self.lineEditOutputFolder.setText(output_folder)

    def writedata(self, ws, tableParameter=None):
        """
        write the data from the table into an excell file.
        :param ws:WorkSheet object from xwlt module for interacts with excell files.
        :param tableParameter: QTableWidget with the information of the data to save.
        """
        if tableParameter is None:
            tableParameter = self.tableParameterOscilogram

        # write the data of the meditions into the stylesheet of excell ws
        styleheader = xlwt.easyxf('font: name Times New Roman, color-index black, bold on, height 300')
        stylebody = xlwt.easyxf('font: name Times New Roman, color-index black, height 220', num_format_str='# ,# # 0.00')
        stylecopyrigth = xlwt.easyxf('font: name Arial, color-index pale_blue, height 250, italic on',
                                     num_format_str='# ,# # 0.00')

        # write headers into the document
        headers = [str(tableParameter.takeHorizontalHeaderItem(pos).text()) for pos in
                   range(tableParameter.columnCount())]

        for index, header in enumerate(headers):
            ws.write(0, index, header, styleheader)

        # write data into the document
        for i in range(1, tableParameter.model().rowCount() + 1):
            for j in range(tableParameter.model().columnCount()):
                if tableParameter.item(i - 1, j):
                    ws.write(i, j, str(tableParameter.item(i - 1, j).data(Qt.DisplayRole).toString()), stylebody)
                else:
                    ws.write(i, j, unicode(self.tr(u"No Identified")), stylebody)

        # ws object must be part of a Woorkbook that would be saved later
        ws.write(tableParameter.model().rowCount() + 3, 0, unicode(self.tr(u"duetto-Sound Lab")),
                 stylecopyrigth)

    # endregion

    # region Close and Exit

    @pyqtSlot()
    def on_actionExit_triggered(self):
        """
        Process the exit action requested by the user.
        :return:
        """
        self.close()

    def closeEvent(self, event):
        """
        Event that manages the close of the window.
        Intercepts the close event for save changes.
        :param event:
        :return:
        """

        mbox = QtGui.QMessageBox(QtGui.QMessageBox.Question, self.tr(u"Save meditions"),
                                 self.tr(u"Do you want to save the meditions?"),
                                 QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, self)

        # if there is a medition made and parameters measured that could be saved
        if self.tableParameterOscilogram.rowCount() > 0:
            # if the signal was playing must be stopped
            self.widget.stop()

            result = mbox.exec_()
            # get the user decision
            if result == QtGui.QMessageBox.Cancel:
                # cancel the close
                event.ignore()
                return

            elif result == QtGui.QMessageBox.Yes:
                # save the measured data as excel
                wb = xlwt.Workbook()
                ws = wb.add_sheet(self.widget.signalName())
                self.writedata(ws, self.tableParameterOscilogram)

                # get the file name to save the meditions
                fname = unicode(QFileDialog.getSaveFileName(self,
                                self.tr(u"Save meditions as excel file"),
                                self.widget.signalName() + ".xls", "*.xls"))
                if fname:
                    wb.save(fname)

            self.clearTwoDimensionalWindows()

    # endregion

    # region Elements Selection

    @pyqtSlot()
    def on_actionClear_Meditions_triggered(self):
        """
        Clear all the detections made. Clear the elements on the widget,
        the meditions on the table and update the
        :return:
        """
        # clear the widget elements detection and its visual figures
        self.widget.clearDetection()

        # clear the two dimensional window asociated with the elements detected
        self.clearTwoDimensionalWindows()

        # refresh the changes
        self.widget.graph()

    @pyqtSlot()
    def on_actionDelete_Selected_Elements_triggered(self):
        """
        Delete the element under selection.
        the selection is the area under the zoom cursor if the zoom cursor is selected
        or the visible area otherwise.
        :return:
        """

        # delete the elements on the widget and get the indexes for update
        deleted_elements = self.widget.deleteSelectedElements()

        if deleted_elements is None:
            return

        start_removed_index, end_removed_index = deleted_elements
        # TODO complete the coment here
        if start_removed_index is not None and start_removed_index >= 0 and end_removed_index < self.tableParameterOscilogram.rowCount():
            for i in range(end_removed_index, start_removed_index - 1, -1):
                # delete from table
                self.tableParameterOscilogram.removeRow(i)

            for i in range(self.tableParameterOscilogram.rowCount()):
                # update table bacground color
                for j in range(self.tableParameterOscilogram.columnCount()):
                    self.tableParameterOscilogram.item(i, j).setBackgroundColor(
                        self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)

            # updates the numpy array  with the detected parameters
            self.measuredParameters = np.concatenate(
                (
                    self.measuredParameters[:start_removed_index[0]], self.measuredParameters[start_removed_index[1] + 1:]))
            self.elementsClasificationTableData = self.elementsClasificationTableData[
                                                  :start_removed_index[0]] + self.elementsClasificationTableData[
                                                                             start_removed_index[1] + 1:]

            self.tableParameterOscilogram.update()
            for wnd in self.two_dim_windows:
                wnd.loadData(self.columnNames, self.measuredParameters)

        # deselect the elements on the widget
        self.on_actionDeselect_Elements_triggered()

    @pyqtSlot()
    def on_actionDeselect_Elements_triggered(self):
        """
        Deselects the selected element in the widget and in the
        two dimensional windows opened.
        :return:
        """
        self.widget.deselectElement()

        for wnd in self.two_dim_windows:
            wnd.deselectElement()

    # endregion

    @pyqtSlot()
    def on_actionFull_Screen_triggered(self):
        """
        Switch the visualization of the window in full screen - normal.
        """
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()