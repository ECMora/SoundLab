# -*- coding: utf-8 -*-
import os

from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4 import QtGui
import xlwt
from PyQt4.QtGui import QFileDialog, QAbstractItemView, QActionGroup

from duetto.audio_signals.AudioSignal import AudioSignal
from sound_lab_core.Elements.Element import Element
from ..dialogs.elemDetectSettings import ElemDetectSettingsDialog
from graphic_interface.windows.TwoDimensionalAnalisysWindow import TwoDimensionalAnalisysWindow
from graphic_interface.windows.ui_python_files.SegmentationAndClasificationWindowUI import Ui_MainWindow
from graphic_interface.dialogs.EditCategoriesDialog import EditCategoriesDialog
from SoundLabWindow import SoundLabWindow
from sound_lab_core.Segmentation.SegmentManager import SegmentManager


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

        self.configureToolBarActionsGroups()

        # the segmentation window do not allow to record a signal
        self.actionRecord.setEnabled(False)

        # the object that handles the measuring of parameters and manage the segments
        self.segmentManager = SegmentManager()
        self.segmentManager.measurementsChanged.connect(lambda: self.updateTableParameter())

        # set the signal to the widget
        self.widget.signal = signal
        self.segmentManager.signal = signal

        # set the configurations for the name of the signal and the visible label
        self.updateSignalPropertiesLabel(signal)
        self.signalNameLineEdit.setReadOnly(True)
        self.actionSignalName.setText(self.widget.signalName)

        # set visible the two graphs by default
        self.changeWidgetsVisibility(True, True)

        # connect the signals on the widget for new detected data by its tools
        # and to select the element in the table. Binding the element click to the table
        self.widget.toolDataDetected.connect(self.updateStatusBar)
        self.widget.elementClicked.connect(self.selectElement)

        self.dockWidgetParameterTableOscilogram.setVisible(False)
        self.tableParameterOscilogram.setSelectionBehavior(QAbstractItemView.SelectRows)

        # add the context menu actions to the widget
        self.__addContextMenuActions()

        # create the progress bar that is showed while the detection is made
        self.windowProgressDetection = QtGui.QProgressBar(self)
        self.setProgressBarVisibility(False)

        # array of windows with two dimensional graphs.
        self.two_dim_windows = []

        self.showMaximized()

        self.restorePreviousSession()

    def restorePreviousSession(self):
        """
        Restore (if any) the previous session with this file.
        That means detected elements, measured parameters etc that are saved on the signal
        extra data.
        :return:
        """
        if not self.widget.signal.extraData:
            return

        data = self.widget.signal.extraData
        # try to add the detected elements from the extra data (list of tuples (start,end) )
        if not isinstance(data, list):
            return

        elements = [e for e in data if isinstance(e, tuple) and len(e) == 2
                    and isinstance(e[0], int) and isinstance(e[1], int)]
        if len(elements) > 0:
            buttons_box = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
            mbox = QtGui.QMessageBox(QtGui.QMessageBox.Question, self.tr(u"soundLab"),
                                     self.tr(u"The file has segmentation data stored. Do you want to load it?"),
                                     buttons_box, self)
            result = mbox.exec_()

            if result == QtGui.QMessageBox.Yes:
                for element in elements:
                    self.widget.markRegionAsElement(element, update=False)
                    self.widget.graph()

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
                self.actionMeditions,
                self.actionView_Parameters,
                self.actionAddElement,
                separator2,

                # change tools actions
                self.actionZoom_Cursor,
                self.actionPointer_Cursor,
                self.actionRectangular_Cursor,
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
                                    self.actionDeselect_Elements, self.actionAddElement, sep]

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
        if self.segmentManager.rowCount == 0 or len(self.segmentManager.parameterColumnNames) == 0:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"The two dimensional analyses window requires at least "
                                              u"one detected element with one parameter measurement."))
            return

        wnd = TwoDimensionalAnalisysWindow(self, self.segmentManager)

        # connect the signals for update the new two dim window actions
        wnd.elementSelected.connect(self.selectElement)
        wnd.elementsClasiffied.connect(self.elementsClasification)

        # load the workspace in the new two dimensional window
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
        # close the opened windows
        for window in self.two_dim_windows:
            window.close()

        # clear the list of two dimensional windows
        self.two_dim_windows = []

    # endregion

    # region Save Measurements

    @pyqtSlot()
    def on_actionMeditions_triggered(self, name="", table=None):
        """
        Save to disc the measurement made by the window to the elements detected.
        :param name: The name of the file to save the data
        :param table: The table with the parameter to save into excel
        :return:
        """
        # get the file name to save the data into.
        file_name = name

        if file_name == "":
            file_name = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save measurements as excel file"),
                                os.path.join(self.workSpace.lastOpenedFolder,
                                str(self.widget.signalName) + ".xls"), "*.xls"))

        # save the data of table
        if file_name:
            # the excel book to save data
            try:

                wb = xlwt.Workbook()
                ws = wb.add_sheet(self.tr(u"Elements Measurements"))
                self.writeData(ws, table)
                wb.save(file_name)

            except Exception as ex:
                print("Error saving the excel file. " + ex.message)

    @pyqtSlot()
    def on_actionSound_File_Segmentation_triggered(self):
        """
        Save the signal into file. Store the segmentation values
        (list of tuples start,end with the indexes of detected element)
        :return:
        """
        if self.segmentManager.rowCount == 0:
            return

        self.widget.saveElementsOnSignal()

        # save the signal to file
        if self.widget.signalFilePath:
            self.widget.save()
        else:
            file_name = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save signal"),
                                                            os.path.join(self.workSpace.lastOpenedFolder,
                                                            str(self.widget.signalName)), u"*.wav"))
            if file_name:
                self.widget.save(file_name)
                self.widget.signalFilePath = file_name

    def setSignalFile(self, file_path=''):
        """
        Update the data of the current signal file path origin in the widget
        (if any)
        :param file_path:
        :return:
        """
        self.widget.signalFilePath = file_path

    def writeData(self, ws, tableParameter):
        """
        Write the data from the table into an excel file stylesheet.
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

        # ws object must be part of a Work book that would be saved later
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

        # if there is a measurement made and parameters measured that could be saved
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
                self.on_actionMeditions_triggered()

            self.clearTwoDimensionalWindows()

    # endregion

    # region Elements Selection

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

        if start_removed_index is not None and start_removed_index >= 0 \
           and end_removed_index < self.segmentManager.rowCount:
            # updates the detected elements
            self.segmentManager.deleteElements(start_removed_index, end_removed_index)

            for wnd in self.two_dim_windows:
                wnd.updateData(self.segmentManager)

        # deselect the elements on the widget
        self.on_actionDeselect_Elements_triggered()

    @pyqtSlot()
    def on_actionAddElement_triggered(self):
        """
        Try to add the selected region on the widget as a new element
        Performs the manual segmentation.
        :return:
        """
        element_added_index = self.widget.markRegionAsElement()

        if element_added_index is None:
            return

        self.segmentManager.addElement(self.widget.elements[element_added_index], element_added_index)

        for wnd in self.two_dim_windows:
            wnd.loadData(self.segmentManager)

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

        # the table remains equal as before for efficiency (do not update for deselect)

    def selectElement(self, element_index, column=0):
        """
        Callback that is executed for update the element that is selected.
        An element is selected by the user ad must be updated in all visible representations
        like table parameter, two dimensional windows, and graphs.
        :param element_index: index of the element selected
        :param column: parameter provided to reuse this method as callback of
        the event selected cell in the QTableWidget. Useless in this application context.
        """
        # select the element in the table of measurements
        self.tableParameterOscilogram.selectRow(element_index)

        # in the widget...
        self.widget.selectElement(element_index)

        # and in the opened two dimensional windows
        for wnd in self.two_dim_windows:
            wnd.selectElement(element_index)

    # endregion

    # region Classification

    @pyqtSlot()
    def on_actionClassification_Settings_triggered(self):
        """
        Open the classification dialog for update the categories and values
        in which could be classified a segment.
        """
        # create and open the dialog to edit the classification categories
        edit_categ_dialog = EditCategoriesDialog(self.segmentManager.classificationData)
        edit_categ_dialog.exec_()

    def elementsClasification(self, indexes_list, dictionary):
        """
        Update the classification of the detected elements on the table manually
        :param indexes_list: the indexes of the classified elements
        :param dictionary: the dictionary with the values of each category
        :return:
        """
        self.segmentManager.classifyElements(indexes_list, dictionary)

    # endregion

    # region Detection

    def updateDetectionProgressBar(self, x):
        """
        update the detection progress bar.
        detection progress bar provides a visible interface
        of the execution progress of consuming time actions such detection and classification.

        :param x: Value to set in the progress bar
        """
        self.windowProgressDetection.setValue(x)

    def setProgressBarVisibility(self, visibility=True):
        """
        Show the progress bar in the middle of the widget.
        Used when a high time demanding task is going to be made to
        show to the user it's progress.
        :return:
        """
        if visibility:
            width, height = self.widget.width(), self.widget.height()
            x, y = self.widget.x(), self.widget.y()

            self.windowProgressDetection.resize(width / 3, 20)
            self.windowProgressDetection.move(x + width / 3, y - height / 2)
            self.windowProgressDetection.setVisible(True)
        else:
            self.windowProgressDetection.setVisible(False)

        self.update()

    @pyqtSlot()
    def on_actionDetection_triggered(self):
        """
        Method that execute the detection
        """
        elementsDetectorDialog = ElemDetectSettingsDialog(parent=self, signal=self.widget.signal)
        elementsDetectorDialog.load_workspace(self.workSpace)

        # deselect the elements
        self.on_actionDeselect_Elements_triggered()

        try:
            if elementsDetectorDialog.exec_():
                # the detection dialog is a factory of segmentation,
                # parameter measurements and classification concrete implementations

                # get the detector from dialog selection
                self.segmentManager.detector = elementsDetectorDialog.detector

                self.segmentManager.measurerList = elementsDetectorDialog.get_measurer_list()
                # get the classification object

                self.setProgressBarVisibility(True)

                # execute the detection
                self.segmentManager.detectElements()
                self.widget.elements = self.segmentManager.elements

                self.updateDetectionProgressBar(50)

                # measure the parameters over elements detected
                self.segmentManager.measureParameters()

                self.updateDetectionProgressBar(95)

                # update the measured data on the two dimensional opened windows
                for wnd in self.two_dim_windows:
                    wnd.loadData(self.segmentManager)

            # refresh changes
            self.widget.graph()

        except Exception as e:
            print("detection errors: " + e.message)

        # complete the progress of detection and hide the progress bar
        self.updateDetectionProgressBar(100)
        self.setProgressBarVisibility(False)

    def updateTableParameter(self):
        """
        Method that updates the parameter table to visualize
        the data of the detected segments, their masured parameters and classification
        :return:
        """
        # set the number of columns to the amount of parameters measured
        # plus the amount of categories of classification
        self.tableParameterOscilogram.clear()
        self.tableParameterOscilogram.setRowCount(self.segmentManager.rowCount)
        self.tableParameterOscilogram.setColumnCount(self.segmentManager.columnCount)
        self.tableParameterOscilogram.setHorizontalHeaderLabels(self.segmentManager.columnNames)

        # update every x,y position
        for i in range(self.segmentManager.rowCount):
            for j in range(self.segmentManager.columnCount):
                # set the result to a table item and save it on the table
                item = QtGui.QTableWidgetItem(unicode(self.segmentManager.getData(i, j)))

                # color options for the rows of the table
                item.setBackgroundColor(self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)
                self.tableParameterOscilogram.setItem(i, j, item)

        # connect the table selection with the selection of an element
        self.tableParameterOscilogram.cellPressed.connect(self.selectElement)
        self.tableParameterOscilogram.resizeColumnsToContents()

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
        self.widget.changeElementsVisibility(self.actionElements_Peaks.isChecked(),
                                             Element.PeakFreqs, oscilogramItems=False)

    @pyqtSlot()
    def on_actionTemporal_Elements_triggered(self):
        """
        Temporal Elements are the elements that are visible on the oscilogram graph.
        This method allows to change its visibility
        """
        visibility = self.actionTemporal_Elements.isChecked()
        for e in self.widget.elements:
            e.visible = visibility
        self.widget.drawElements(oscilogramItems=True)

        self.actionTemporal_Figures.setEnabled(visibility)
        self.actionTemporal_Numbers.setEnabled(visibility)

    @pyqtSlot()
    def on_actionTemporal_Numbers_triggered(self):
        """
        Change visibility of the numbers of the detected segments on the oscilogram graph

        """
        self.widget.changeElementsVisibility(self.actionTemporal_Numbers.isChecked(), Element.Text)

    @pyqtSlot()
    def on_actionSpectral_Numbers_triggered(self):
        """
        Change visibility of the numbers of the detected segments on the spectrogram graph
        """
        self.widget.changeElementsVisibility(self.actionSpectral_Numbers.isChecked(),
                                             Element.Text, oscilogramItems=False)

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
        for e in self.widget.elements:
            for e2 in e.twoDimensionalElements:
                e2.visible = visibility
        self.widget.drawElements(oscilogramItems=False)
        self.actionSpectral_Figures.setEnabled(visibility)
        self.actionSpectral_Numbers.setEnabled(visibility)
        self.actionSub_Elements_Peaks.setEnabled(visibility)

    # endregion

    def load_workspace(self, workspace):
        """
        Method that loads the workspace to update visual options from main window.
        :param workspace:
        """
        self.workSpace = workspace
        self.widget.load_workspace(workspace)

        # update workspace on every window
        for wnd in self.two_dim_windows:
            wnd.load_workspace(self.workSpace)