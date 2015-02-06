# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSlot, Qt
import PyQt4.QtCore as QtCore
from PyQt4 import QtGui
import xlwt
import numpy as np
from PyQt4.QtGui import QFileDialog, QAbstractItemView, QWidget, QActionGroup
from pyqtgraph.parametertree import Parameter
from duetto.audio_signals.AudioSignal import AudioSignal
from sound_lab_core.Clasification.ClassificationData import ClassificationData
from sound_lab_core.Segmentation.Elements.Element import Element
from sound_lab_core.Segmentation.Elements.OneDimensionalElements.OneDimensionalElement import SpectralMeasurementLocation
from ..dialogs.elemDetectSettings import ElemDetectSettingsDialog
from graphic_interface.windows.TwoDimensionalAnalisysWindow import TwoDimensionalAnalisysWindow
from graphic_interface.windows.ui_python_files.SegmentationAndClasificationWindowUI import Ui_MainWindow
import graphic_interface.windows.ui_python_files.EditCategoriesDialogUI as editCateg
from graphic_interface.dialogs.EditCategoriesDialog import EditCategoriesDialog
from graphic_interface.widgets.EditCategoriesWidget import EditCategoriesWidget
from SoundLabWindow import SoundLabWindow


class SegmentManager:
    """
    Manage the parameter measurement over a group of segments.
    Provide a table interface for segments parameter measurement and classification
    """
    def __init__(self):
        # the classifier object that
        self._classifier = None

        # the parameter measurer list
        self._measurer = None

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

    def getData(self, row, col):
        """
        """
        if row >= len(self.measuredParameters):
            raise IndexError()


        return self.measuredParameters[row,col]

    # region Properties

    # region Classifier

    @property
    def classifier(self):
        return self._classifier

    @classifier.setter
    def classifier(self, classifier):
        self._classifier = classifier

    # endregion

    # region Measurer

    @property
    def measurer(self):
        return self._measurer

    @measurer.setter
    def measurer(self, new_measurer):
        self._measurer = new_measurer

    # endregion

    # endregion

    # region Classification
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
            self.segmentManager.elementsClasificationTableData[i].append([str(category), self.tr(u"No Identified")])

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
    # endregion

    def addSegment(self, segment):
        """
        Add a new segment to the list of detected elements on the
        manager. if a parameter measurer is selected
        """
        pass



class Segmentation_ClassificationWindow(SoundLabWindow, Ui_MainWindow):
    """
    Window that process the segmentation and classification of a signal
    Contains a QSignalDetectorWidget that wrapper several functionality
    Allows to select the segmentation and classification settings,
    and parameter measurement for detected segments.
    Provides a table for visualization of segment and measures,
    A two dimensional window to graph two measured params. One for each axis.
    Options for selection and visualization of segments
    Provides options for save the measurements to excel.
    """

    # region CONSTANTS
    # different colors for the even and odds rows in the parameter table and segment colors.
    TABLE_ROW_COLOR_ODD = QtGui.QColor(0, 0, 255, 150)
    TABLE_ROW_COLOR_EVEN = QtGui.QColor(0, 255, 0, 150)

    # stylesheet to use on excel file saved
    EXCEL_STYLE_HEADER = xlwt.easyxf('font: name Times New Roman, color-index black, bold on, height 300')
    EXCEL_STYLE_BODY = xlwt.easyxf('font: name Times New Roman, color-index black, height 220', num_format_str='# ,# # 0.00')
    EXCEL_STYLE_COPYRIGHT = xlwt.easyxf('font: name Arial, color-index pale_blue, height 250, italic on', num_format_str='# ,# # 0.00')
    # endregion

    # region Initialize

    def __init__(self, parent, signal):
        """
        Create a the window of segmentation and clasiffication.
        :param parent: the parent widget if any
        :param signal: the signal to visualize for segmentation and clasiffication
        :return:
        """
        # set the visual variables and methods from ancestor's
        SoundLabWindow.__init__(self, parent)
        self.setupUi(self)

        # check the parameters
        if signal is None or not isinstance(signal, AudioSignal):
            raise Exception("The signal to analyze must be of type AudioSignal")

        self.ParamTree = self.getParamTree()

        self.configureToolBarActionsGroups()

        # the segmentation window do not allow record or signal name edition
        self.updateSignalPropertiesLabel(signal)
        self.signalNameLineEdit.setReadOnly(True)

        self.actionRecord.setEnabled(False)

        # set the signal to the widget
        self.widget.signal = signal

        # set visible the two widgets by default
        self.changeWidgetsVisibility(True, True)

        # connect the signal of the widget for new detected data by its tools
        self.widget.toolDataDetected.connect(self.updateStatusBar)

        self.dockWidgetParameterTableOscilogram.setVisible(False)
        self.tableParameterOscilogram.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.spectralMeasurementLocation = SpectralMeasurementLocation()

        # for select the element in the table. Binding for the element click to the table
        self.widget.elementClicked.connect(self.elementSelectedInTable)

        # add the context menu actions to the widget
        self.__addContextMenuActions()

        # create the progress bar that is showed while the detection is made
        self.windowProgressDetection = QtGui.QProgressBar(self.widget)
        self.setProgressBarVisibility(False)

        # set the name of the signal to the visible label
        self.actionSignalName.setText(self.widget.signalName)

        # array of windows with two dimensional graphs.
        # Are stored for a similar behavior to the one dimensional
        # in the main window. Updates the windows graphs on change etc
        self.two_dim_windows = []

        self.segmentManager = SegmentManager()

        self.showMaximized()

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

        self.meditions = [(unicode(self.tr(u'Temporal Meditions')), self.timeMeditions), \
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

        return Parameter.create(name=u'params', type=u'group', children=params)

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
                self.actionOsc_Image,
                self.actionSpecgram_Image,
                self.actionCombined_Image])
        # endregion

    def configureToolBarActionsGroups(self):
        """
        :return:
        """
        sep = QtGui.QAction(self)
        sep.setSeparator(True)

        # region Segmentation and Transformations actions
        segm_transf_actions = QActionGroup(self)
        segm_transf_actions_list = [self.actionDetection, self.actionTwo_Dimensional_Graphs,
                                    self.actionDelete_Selected_Elements,
                                    self.actionDeselect_Elements, sep]

        for act in segm_transf_actions_list:
            act.setActionGroup(segm_transf_actions)

        # endregion

        # add to the customizable sound lab toolbar first than the default actions
        #            addActionGroup(actionGroup, name)
        self.toolBar.addActionGroup(segm_transf_actions, u"Segments")

        # apply the common sound lab window toolbar actions
        SoundLabWindow.configureToolBarActionsGroups(self)

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

        wnd = TwoDimensionalAnalisysWindow(self, columns=self.segmentManager.columnNames, data=self.segmentManager.measuredParameters,
                                           classificationData=self.segmentManager.classificationData)

        # connect the signals for update the new two dim window actions
        wnd.elementSelected.connect(self.elementSelectedInTable)
        wnd.elementsClasiffied.connect(self.elementsClasification)

        # load the theme in the new two dimensional window
        if self.workSpace:
            wnd.load_workspace(self.workSpace)

        # if any previous windows was opened then update in the new one the selected element
        if len(self.two_dim_windows) > 0:
            wnd.selectElement(self.two_dim_windows[0].selectedElementIndex)

        # add the new window to the current opened windows
        self.two_dim_windows.append(wnd)

    def clearTwoDimensionalWindows(self):
        """
        Close the two dimensional windows and clear the list of two dim windows
        :return:
        """
        # close the open windows
        for window in self.two_dim_windows:
            window.close()

        # initialize the list
        self.two_dim_windows = []

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

    # region Save Measurements as Excel

    @pyqtSlot()
    def on_actionMeditions_triggered(self, name="", table=None):
        """
        Save to disc the measurement made by the window to the elements detected.
        :param name: The name of the file to save the data
        :param table: The table with the parameter to save into excel
        :return:
        """
        # get the file name to save the data into.
        fname = name if name != "" else unicode(QFileDialog.getSaveFileName(self,
                                                self.tr(u"Save measurements as excel file"),
                                                self.widget.signalName + ".xls", "*.xls"))
        # save the data of table
        if fname:
            # the excel book to save data
            self.saveAsExcel(table, fname, self.tr(u"Elements Measurements"))

    def saveAsExcel(self, table, file_name, excel_sheet_name):
        """
        Save in an excel file the data stored in the table
        :param table: A table widget with the data to save
        :param file_name: The file name to save the data.
        :return:
        """
        try:

            wb = xlwt.Workbook()
            ws = wb.add_sheet(unicode(excel_sheet_name))
            self.writeData(ws, table)
            wb.save(file_name)

        except Exception as ex:
            print("Error saving the excel file. "+ex.message)

    def writeData(self, ws, tableParameter):
        """
        write the data from the table into an excel file.
        :param ws:WorkSheet object from xwlt module for interacts with excell files.
        :param tableParameter: QTableWidget with the information of the data to save.
        """
        # write headers into the document
        headers = [str(tableParameter.takeHorizontalHeaderItem(pos).text()) for pos in
                   range(tableParameter.columnCount())]

        for index, header in enumerate(headers):
            ws.write(0, index, header, self.EXCEL_STYLE_HEADER)

        # write data into the document
        for i in range(1, tableParameter.model().rowCount() + 1):
            for j in range(tableParameter.model().columnCount()):
                if tableParameter.item(i - 1, j):
                    ws.write(i, j, str(tableParameter.item(i - 1, j).data(Qt.DisplayRole).toString()), self.EXCEL_STYLE_BODY)
                else:
                    ws.write(i, j, unicode(self.tr(u"No Identified")), self.EXCEL_STYLE_BODY)

        # ws object must be part of a Woorkbook that would be saved later
        ws.write(tableParameter.model().rowCount() + 3, 0, unicode(self.tr(u"duetto-Sound Lab")),
                 self.EXCEL_STYLE_COPYRIGHT)

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
                                 self.tr(u"Do you want to save the measurements of "+unicode(self.widget.signalName)),
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
                # get the file name to save the meditions
                fname = unicode(QFileDialog.getSaveFileName(self,
                                self.tr(u"Save meditions as excel file"),
                                self.widget.signalName + ".xls", "*.xls"))
                if fname:
                    self.saveAsExcel(self.tableParameterOscilogram, fname, self.widget.signalName)

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
        # TODO complete the comment here
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
            self.segmentManager.measuredParameters = np.concatenate(
                (
            self.segmentManager.measuredParameters[:start_removed_index[0]], self.segmentManager.measuredParameters[start_removed_index[1] + 1:]))
            self.segmentManager.elementsClasificationTableData = self.segmentManager.elementsClasificationTableData[
                                                  :start_removed_index[0]] + self.segmentManager.elementsClasificationTableData[
                                                                             start_removed_index[1] + 1:]

            self.tableParameterOscilogram.update()
            for wnd in self.two_dim_windows:
                wnd.loadData(self.segmentManager.columnNames, self.segmentManager.measuredParameters)

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

        for k in self.segmentManager.classificationData.categories.keys():
            # foreach clasification category add a widget to show it
            widget = EditCategoriesWidget(self, k, self.segmentManager.classificationData)
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
            if self.clasiffCategories_vlayout and self.segmentManager.classificationData.addCategory(category):
                self.clasiffCategories_vlayout.addWidget(EditCategoriesWidget(self, category, self.segmentManager.classificationData))

    def elementsClasification(self, indexes_list, dictionary):
        """
        Update the clasificaction of the detected elements on the table
        :param indexes_list: the indexes of the classified elements
        :param dictionary: the dictionary with the values of each category
        :return:
        """
        for i in indexes_list:
            for column, l in enumerate(self.segmentManager.elementsClasificationTableData[i]):
                if l[0] in dictionary:
                    self.segmentManager.elementsClasificationTableData[i][column][1] = dictionary[l[0]]
                    item = QtGui.QTableWidgetItem(unicode(self.segmentManager.elementsClasificationTableData[i][column][1]))
                    item.setBackgroundColor(
                        self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)
                    self.tableParameterOscilogram.setItem(i, len(self.segmentManager.measuredParameters[i]) + column, item)

        # resize the column to contains completely the new categories and values
        self.tableParameterOscilogram.resizeColumnsToContents()
        self.tableParameterOscilogram.update()

    # endregion

    # region Detection

    def getSettings(self, elementsDetectorDialog):
        """
        get the detection settings
        :param elementsDetectorDialog: dialog that contains the parameter tree with all the options
        :return:
        """
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
        elementsDetectorDialog = ElemDetectSettingsDialog(parent=self,paramTree=self.ParamTree, signal=self.widget.signal)
        elementsDetectorDialog.load_workspace(self.workSpace)

        # deselect the elements on the widget
        self.widget.deselectElement()
        try:
            if elementsDetectorDialog.exec_():
                self.getSettings(elementsDetectorDialog)

                # get the detector from dialog selection
                self.widget.detector = elementsDetectorDialog.detector

                paramsTomeasure = self.getParameters()

                self.setProgressBarVisibility(True)

                # execute the detection
                self.widget.detectElements()

                self.updateDetectionProgressBar(50)

                # clasification data update TODO improve comments and implementation
                validcategories = [k for k in self.segmentManager.classificationData.categories.keys() if
                                   len(self.segmentManager.classificationData.getvalues(k)) > 0]

                self.segmentManager.elementsClasificationTableData = [[[k, self.tr(u"No Identified")] for k in validcategories] for
                                                       _ in range(self.tableParameterOscilogram.rowCount())]

                # clear the previous meditions
                self.tableParameterOscilogram.clear()

                elem_count = len(self.widget.Elements)
                parameter_count = len(paramsTomeasure)

                self.tableParameterOscilogram.setRowCount(elem_count)

                # connect the table selection with the selection of an element
                self.tableParameterOscilogram.cellPressed.connect(self.elementSelectedInTable)

                # get the column names of the meditions and set them on the table headers
                self.segmentManager.columnNames = [label[0] for label in paramsTomeasure]

                columns = self.segmentManager.columnNames + validcategories

                # set the number of columns to the amount of parameters measured
                # plus the amount of categories of classification
                self.tableParameterOscilogram.setColumnCount(len(columns))
                self.tableParameterOscilogram.setHorizontalHeaderLabels(columns)

                self.updateDetectionProgressBar(95)

                # the table of parameters stored as a numpy array
                self.segmentManager.measuredParameters = np.zeros(elem_count * parameter_count).reshape((elem_count, parameter_count))

                self.measureParameters(paramsTomeasure, validcategories)

                # complete the progress of detection and hide the progress bar
                self.updateDetectionProgressBar(100)
                self.setProgressBarVisibility(False)
                self.tableParameterOscilogram.resizeColumnsToContents()

                # update the measured data on the two dimensional opened windows
                for wnd in self.two_dim_windows:
                    wnd.loadData(self.segmentManager.columnNames, self.segmentManager.measuredParameters)

            # refresh changes
            self.widget.graph()

        except Exception as e:
            print("detection errors: " + e.message)

    def measureParameters(self, paramsTomeasure, validcategories ):
        for i in range(self.tableParameterOscilogram.rowCount()):
            for j, params in enumerate(paramsTomeasure):
                try:
                    # get the function params.
                    # params[0] is the name of the param measured
                    # params[1] is the function to measure the param
                    # params[2] is the dictionary of params supplied to the function
                    dictionary = dict(params[2] if params[2] is not None else [])

                    # compute the param with the function
                    self.segmentManager.measuredParameters[i, j] = params[1](self.widget.Elements[i], dictionary)

                    # set the result to a table item and save it on the table
                    item = QtGui.QTableWidgetItem(unicode(self.segmentManager.measuredParameters[i, j]))

                    # color options for the rows of the table
                    item.setBackgroundColor(
                        self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)

                except Exception as e:
                    # if some error is raised set a default value
                    item = QtGui.QTableWidgetItem(0)
                    print("Error measure params " + e.message)

                self.tableParameterOscilogram.setItem(i, j, item)

            for c in range(len(validcategories)):
                try:
                    val = self.segmentManager.elementsClasificationTableData[i][c][1]
                    item = QtGui.QTableWidgetItem(unicode(val))
                    item.setBackgroundColor(
                        self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)

                except Exception as e:
                    # if some error is raised set a default value
                    item = QtGui.QTableWidgetItem(0)
                    print("Error measure params " + e.message)

            self.tableParameterOscilogram.setItem(i, c + len(paramsTomeasure), item)

    def setProgressBarVisibility(self, visibility=True):
        """
        Show the progress bar in the middle of the widget.
        Used when a high time demanding task is going to be made to
        show to the user it's progress.
        :return:
        """
        if visibility:
            width, height = self.widget.width(), self.windowProgressDetection.size().height()
            x, y = self.widget.x(), self.widget.y()

            self.windowProgressDetection.resize(width / 3, height)
            self.windowProgressDetection.move(x + width / 3, y - height / 2 + width / 2)
            self.windowProgressDetection.show()
        else:
            self.windowProgressDetection.hide()

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