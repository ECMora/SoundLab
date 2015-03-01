# -*- coding: utf-8 -*-
import os
import xlwt
from PyQt4.QtCore import pyqtSlot, Qt
from SoundLabWindow import SoundLabWindow
from graphic_interface.segment_visualzation.VisualElement import VisualElement
from duetto.audio_signals.AudioSignal import AudioSignal
from graphic_interface.dialogs.CrossCorrelationDialog import CrossCorrelationDialog
from ..dialogs.elemDetectSettings import ElemDetectSettingsDialog
from sound_lab_core.Segmentation.SegmentManager import SegmentManager
from ..dialogs.ManualClassificationDialog import ManualClassificationDialog
from TwoDimensionalAnalisysWindow import TwoDimensionalAnalisysWindow
from ui_python_files.SegmentationAndClasificationWindowUI import Ui_MainWindow
from PyQt4.QtGui import QFileDialog, QAbstractItemView, QActionGroup, QMessageBox, \
    QProgressBar, QColor, QAction, QTableWidgetItem


class SegmentationClassificationWindow(SoundLabWindow, Ui_MainWindow):
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
    TABLE_ROW_COLOR_ODD = QColor(0, 0, 255, 150)
    TABLE_ROW_COLOR_EVEN = QColor(0, 255, 0, 150)

    # stylesheet to use on excel file saved
    EXCEL_STYLE_HEADER = xlwt.easyxf('font: name Times New Roman, color-index black, bold on, height 300')
    EXCEL_STYLE_BODY = xlwt.easyxf('font: name Times New Roman, color-index black, height 220',
                                   num_format_str='#,# # 0.00')
    EXCEL_STYLE_COPYRIGHT = xlwt.easyxf('font: name Arial, color-index pale_blue, height 250, italic on',
                                        num_format_str='# ,# # 0.00')
    # endregion

    # region Initialize

    def __init__(self, parent, signal):
        """
        Create a the window of segmentation and classification.
        :param parent: the parent widget if any
        :param signal: the signal to visualize for segmentation and classification
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
        self.segmentManager.measurementsChanged.connect(lambda: self.update_parameter_table())
        self.segmentManager.segmentVisualItemAdded.connect(self.widget.add_visual_item)

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
        self.widget.elementClicked.connect(self.select_element)

        self.dockWidgetParameterTableOscilogram.setVisible(False)
        self.tableParameterOscilogram.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableParameterOscilogram.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # add the context menu actions to the widget
        self.__addContextMenuActions()

        # create the progress bar that is showed while the detection is made
        self.windowProgressDetection = QProgressBar(self)
        self.set_progress_bar_visibility(False)

        # array of windows with two dimensional graphs.
        self.two_dim_windows = []
        self._cross_correlation_windows = []

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

        if len(elements) == 0:
            return

        buttons_box = QMessageBox.Yes | QMessageBox.No
        mbox = QMessageBox(QMessageBox.Question, self.tr(u"soundLab"),
                           self.tr(u"The file has segmentation data stored. Do you want to load it?"),
                           buttons_box, self)
        result = mbox.exec_()

        if result == QMessageBox.Yes:
            for element in elements:
                self.widget.mark_region_as_element(element, update=False)
                self.widget.graph()

    def __addContextMenuActions(self):
        """
        Add the context menu actions into the widget in the creation process of the window
        :return:
        """
        separator, separator1, separator2, separator3, separator4 = [QAction(self) for _ in xrange(5)]

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

                # measurements manipulation actions
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
                self.actionSelectedElement_Correlation,
                separator4

                ])
        # endregion

    def configureToolBarActionsGroups(self):
        """
        :return:
        """
        sep = QAction(self)
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
        # addActionGroup(actionGroup, name)
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
        # a two dim window must be created after
        # segment detection and parameters measurement
        if self.segmentManager.rowCount == 0 or len(self.segmentManager.parameterColumnNames) == 0:
            QMessageBox.warning(QMessageBox(), self.tr(u"Error"),
                                self.tr(u"The two dimensional analyses window requires at least "
                                        u"one detected element with one parameter measurement."))
            return

        wnd = TwoDimensionalAnalisysWindow(self, self.segmentManager)

        # connect the signals for update the new two dim window actions
        wnd.elementSelected.connect(self.select_element)
        wnd.elementsClassified.connect(lambda indexes_list, classification_list:
                                       self.segmentManager.set_manual_elements_classification(indexes_list, classification_list))

        # load the workspace in the new two dimensional window
        if self.workSpace:
            wnd.load_workspace(self.workSpace)

        # if any previous windows was opened then update in the new one the selected element
        if len(self.two_dim_windows) > 0:
            wnd.select_element(self.two_dim_windows[0].selectedElementIndex)

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
            del window

        # clear the list of two dimensional windows
        self.two_dim_windows = []

    # endregion

    # region Save Measurements

    @pyqtSlot()
    def on_actionMeditions_triggered(self):
        """
        Save to disc the measurement made by the window to the elements detected.
        :param name: The name of the file to save the data
        :param table: The table with the parameter to save into excel
        :return:
        """
        file_name = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save measurements as excel file"),
                                                        os.path.join(self.workSpace.lastOpenedFolder,
                                                                     str(self.widget.signalName) + ".xls"), "*.xls"))

        # save the data of table
        if file_name:
            # the excel book to save data
            try:

                wb = xlwt.Workbook()
                ws = wb.add_sheet("Elements Measurements")
                self.writeData(ws, self.tableParameterOscilogram)
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

        self.widget.save_segments_into_signal()

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
                   xrange(tableParameter.columnCount())]

        for index, header in enumerate(headers):
            ws.write(0, index, header, self.EXCEL_STYLE_HEADER)

        # write data into the document
        for i in xrange(1, tableParameter.model().rowCount() + 1):
            for j in xrange(tableParameter.model().columnCount()):
                if tableParameter.item(i - 1, j):
                    ws.write(i, j, str(tableParameter.item(i - 1, j).data(Qt.DisplayRole).toString()),
                             self.EXCEL_STYLE_BODY)
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

        mbox = QMessageBox(QMessageBox.Question, self.tr(u"Save meditions"),
                           self.tr(u"Do you want to save the measurements of " + unicode(self.widget.signalName)),
                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, self)

        # if there is a measurement made and parameters measured that could be saved
        if self.tableParameterOscilogram.rowCount() > 0:
            # if the signal was playing must be stopped
            self.widget.stop()

            result = mbox.exec_()
            # get the user decision
            if result == QMessageBox.Cancel:
                # cancel the close
                event.ignore()
                return

            elif result == QMessageBox.Yes:
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
        deleted_elements = self.widget.delete_selected_elements()

        if deleted_elements is None:
            return

        start_removed_index, end_removed_index = deleted_elements

        if start_removed_index is not None and start_removed_index >= 0 \
                and end_removed_index < self.segmentManager.rowCount:
            # updates the detected elements
            self.segmentManager.delete_elements(start_removed_index, end_removed_index)

            for wnd in self.two_dim_windows:
                wnd.update_data(self.segmentManager)

        # deselect the elements on the widget
        self.on_actionDeselect_Elements_triggered()

    @pyqtSlot()
    def on_actionAddElement_triggered(self):
        """
        Try to add the selected region on the widget as a new element
        Performs the manual segmentation.
        :return:
        """
        element_added_index = self.widget.mark_region_as_element()

        if element_added_index is None:
            return

        self.segmentManager.add_element(self.widget.elements[element_added_index], element_added_index)

        for wnd in self.two_dim_windows:
            wnd.load_data(self.segmentManager)

    @pyqtSlot()
    def on_actionDeselect_Elements_triggered(self):
        """
        Deselects the selected element in the widget and in the
        two dimensional windows opened.
        :return:
        """
        self.widget.deselect_element()

        for wnd in self.two_dim_windows:
            wnd.deselect_element()

        # the table remains equal as before for efficiency (do not update for deselect)

    def select_element(self, element_index, column=0):
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
        self.widget.select_element(element_index)

        # in the opened two dimensional windows...
        for wnd in self.two_dim_windows:
            wnd.select_element(element_index)

        # and in the cross-correlation windows
        for i in xrange(len(self._cross_correlation_windows)):
            wnd = self._cross_correlation_windows[i]
            if wnd.isHidden():
                del self._cross_correlation_windows[i]
            else:
                wnd.select_element(element_index)

    # endregion

    # region Classification

    @pyqtSlot()
    def on_actionClassification_Settings_triggered(self):
        """
        Open the classification dialog for update the categories and values
        in which could be classified a segment.
        """
        # create and open the dialog to edit the classification categories
        edit_categ_dialog = ManualClassificationDialog()
        edit_categ_dialog.exec_()

    @pyqtSlot()
    def on_actionCross_correlation_triggered(self):
        """
        Opens the cross-correlation dialog (after selecting a file containing a reference segment) to check each
        segment's match with a reference segment.
        """
        file_name = QFileDialog.getOpenFileName(self, self.tr(u"Select the file of a reference segment"),
                                                directory=self.workSpace.lastOpenedFile,
                                                filter=self.tr(u"Wave Files") + u"(*.wav);;All Files(*)")
        if file_name:
            dialog = CrossCorrelationDialog(self, self.widget, file_name,
                                             self.TABLE_ROW_COLOR_ODD, self.TABLE_ROW_COLOR_EVEN)
            self._cross_correlation_windows.append(dialog)
            dialog.elementSelected.connect(self.select_element)
            dialog.show()

    @pyqtSlot()
    def on_actionSelectedElement_Correlation_triggered(self):
        signal = self.widget.selected_element_signal()
        if not signal:
            QMessageBox.warning(QMessageBox(), self.tr(u"Error"),
                                self.tr(u"There is no selected element."))
            return

        dialog = CrossCorrelationDialog(self, self.widget, signal,
                                         self.TABLE_ROW_COLOR_ODD, self.TABLE_ROW_COLOR_EVEN)

        self._cross_correlation_windows.append(dialog)
        dialog.elementSelected.connect(self.select_element)
        dialog.show()

    # endregion

    # region Detection

    def update_detection_progress_bar(self, x):
        """
        update the detection progress bar.
        detection progress bar provides a visible interface
        of the execution progress of consuming time actions such detection and classification.

        :param x: Value to set in the progress bar
        """
        self.windowProgressDetection.setValue(x)

    def set_progress_bar_visibility(self, visibility=True):
        """
        Show the progress bar in the middle of the widget.
        Used when a high time demanding task is going to be made to
        show to the user it's progress.
        :return:
        """
        if visibility:
            width, height = self.widget.width(), self.widget.height()
            x, y = self.widget.x(), self.widget.y()
            progress_bar_height = height / 20.0

            self.windowProgressDetection.resize(width / 3.0, progress_bar_height)
            self.windowProgressDetection.move(x + width / 3.0, y + height / 2.0 + progress_bar_height / 2.0)
            self.windowProgressDetection.setVisible(True)
        else:
            self.windowProgressDetection.setVisible(False)

        self.repaint()

    @pyqtSlot()
    def on_actionDetection_triggered(self):
        """
        Method that execute the detection
        """
        elementsDetectorDialog = ElemDetectSettingsDialog(parent=self, signal=self.widget.signal)
        elementsDetectorDialog.load_workspace(self.workSpace)
        elementsDetectorDialog.restore_previous_state(self.segmentManager.measurerList,
                                                      self.segmentManager.detector_adapter,
                                                      self.segmentManager.classifier_adapter)

        # deselect the elements before new detection
        self.on_actionDeselect_Elements_triggered()

        try:
            if elementsDetectorDialog.exec_():
                # the detection dialog is a factory of segmentation,
                # parameter measurements and classification concrete implementations

                # get the detector from dialog selection
                self.segmentManager.detector_adapter = elementsDetectorDialog.detector
                self.segmentManager.classifier_adapter = elementsDetectorDialog.classifier
                self.segmentManager.measurerList = elementsDetectorDialog.get_measurer_list()

                self.update_detection_progress_bar(0)
                self.set_progress_bar_visibility(True)

                # set the detection as the 50% of the segmentation,
                # parameter measurements and classification time
                self.segmentManager.detectionProgressChanged.connect(
                    lambda x: self.update_detection_progress_bar(x * 0.5))

                # execute the detection
                self.segmentManager.detect_elements()
                self.update_detection_progress_bar(50)

                self.widget.elements = self.segmentManager.elements

                self.segmentManager.measureParametersProgressChanged.connect(
                    lambda x: self.update_detection_progress_bar(70 + x * 0.2))

                # measure the parameters over elements detected
                self.segmentManager.measure_parameters()
                self.update_detection_progress_bar(90)

                # measure the parameters over elements detected
                self.segmentManager.classify_elements()
                self.update_detection_progress_bar(98)

                # update the measured data on the two dimensional opened windows
                for wnd in self.two_dim_windows:
                    wnd.load_data(self.segmentManager)

                self.widget.graph()

        except Exception as e:
            print("detection errors: " + e.message)
            self.update_parameter_table()

        # complete the progress of detection and hide the progress bar
        self.update_detection_progress_bar(100)
        self.set_progress_bar_visibility(False)

    def update_parameter_table(self):
        """
        Method that updates the parameter table to visualize
        the data of the detected segments, their measured parameters and classification
        :return:
        """
        # set the number of columns to the amount of parameters measured
        # plus the amount of categories of classification
        self.tableParameterOscilogram.clear()
        self.tableParameterOscilogram.setRowCount(self.segmentManager.rowCount)
        self.tableParameterOscilogram.setColumnCount(self.segmentManager.columnCount)
        self.tableParameterOscilogram.setHorizontalHeaderLabels(self.segmentManager.columnNames)
        self.tableParameterOscilogram.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # update every x,y position
        for i in xrange(self.segmentManager.rowCount):
            for j in xrange(self.segmentManager.columnCount):
                # set the result to a table item and save it on the table
                item = QTableWidgetItem(unicode(self.segmentManager[i, j]))

                # color options for the rows of the table
                item.setBackgroundColor(self.TABLE_ROW_COLOR_ODD if i % 2 == 0 else self.TABLE_ROW_COLOR_EVEN)
                self.tableParameterOscilogram.setItem(i, j, item)

        # connect the table selection with the selection of an element
        self.tableParameterOscilogram.cellPressed.connect(self.select_element)
        self.tableParameterOscilogram.resizeColumnsToContents()
        self.tableParameterOscilogram.resizeRowsToContents()

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
    def on_actionTemporal_Elements_triggered(self):
        """
        Temporal Elements are the elements that are visible on the oscilogram graph.
        This method allows to change its visibility
        """
        visibility = self.actionTemporal_Elements.isChecked()
        if visibility:
            self.on_actionTemporal_Numbers_triggered(update_widget=False)
            self.on_actionTemporal_Figures_triggered(update_widget=False)
            self.on_actionTemporal_Parameters_triggered(update_widget=True)
        else:
            self.widget.change_elements_visibility(visibility, VisualElement.Parameters,
                                                   oscilogram_items=True, update=True)
            self.widget.change_elements_visibility(visibility, VisualElement.Text, oscilogram_items=True)
            self.widget.change_elements_visibility(visibility, VisualElement.Figures, oscilogram_items=True)

        self.actionTemporal_Figures.setEnabled(visibility)
        self.actionTemporal_Numbers.setEnabled(visibility)
        self.actionTemporal_Parameters.setEnabled(visibility)

    @pyqtSlot()
    def on_actionTemporal_Figures_triggered(self, update_widget=True):
        self.widget.change_elements_visibility(self.actionTemporal_Figures.isChecked(), VisualElement.Figures,
                                               oscilogram_items=True, update=update_widget)

    @pyqtSlot()
    def on_actionTemporal_Parameters_triggered(self, update_widget=True):
        self.widget.change_elements_visibility(self.actionTemporal_Figures.isChecked(), VisualElement.Parameters,
                                               oscilogram_items=True, update=update_widget)

    @pyqtSlot()
    def on_actionTemporal_Numbers_triggered(self, update_widget=True):
        """
        Change visibility of the numbers of the detected segments on the oscilogram graph

        """
        self.widget.change_elements_visibility(self.actionTemporal_Numbers.isChecked(), VisualElement.Text,
                                               oscilogram_items=True, update=update_widget)

    @pyqtSlot()
    def on_actionSpectral_Elements_triggered(self):
        """
        Spectral Elements are the elements that are visible on the spectrogram graph.
        This method allows to change its visibility
        """
        visibility = self.actionSpectral_Elements.isChecked()
        if visibility:
            self.on_actionSpectral_Numbers_triggered(update_widget=False)
            self.on_actionSpectral_Figures_triggered(update_widget=False)
            self.on_actionSpectral_Parameters_triggered(update_widget=True)
        else:
            self.widget.change_elements_visibility(visibility, VisualElement.Figures, oscilogram_items=False)
            self.widget.change_elements_visibility(visibility, VisualElement.Parameters, oscilogram_items=False)
            self.widget.change_elements_visibility(visibility, VisualElement.Text, oscilogram_items=False, update=True)

        self.actionSpectral_Numbers.setEnabled(visibility)
        self.actionSpectral_Figures.setEnabled(visibility)
        self.actionSpectral_Parameters.setEnabled(visibility)


    @pyqtSlot()
    def on_actionSpectral_Figures_triggered(self,update_widget=True):
        self.widget.change_elements_visibility(self.actionSpectral_Figures.isChecked(), VisualElement.Figures,
                                               oscilogram_items=False, update=update_widget)

    @pyqtSlot()
    def on_actionSpectral_Parameters_triggered(self,update_widget=True):
        self.widget.change_elements_visibility(self.actionSpectral_Parameters.isChecked(), VisualElement.Parameters,
                                               oscilogram_items=False, update=update_widget)

    @pyqtSlot()
    def on_actionSpectral_Numbers_triggered(self,update_widget=True):
        """
        Change visibility of the numbers of the detected segments on the oscilogram graph

        """
        self.widget.change_elements_visibility(self.actionSpectral_Numbers.isChecked(), VisualElement.Text,
                                               oscilogram_items=False, update=update_widget)

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
