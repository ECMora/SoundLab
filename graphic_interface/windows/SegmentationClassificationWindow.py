# -*- coding: utf-8 -*-
import os
import xlwt
from SoundLabWindow import SoundLabWindow
from PyQt4.QtCore import pyqtSlot, Qt, QPoint, QTimer
from duetto.audio_signals.AudioSignal import AudioSignal
from PyQt4.QtGui import QFileDialog, QAbstractItemView, QActionGroup, QMessageBox, \
    QProgressBar, QColor, QAction, QTableWidgetItem
from graphic_interface.windows.ParametersWindow import ParametersWindow
from sound_lab_core.ParametersMeasurement.MeasurementTemplate import MeasurementTemplate
from graphic_interface.dialogs.CrossCorrelationDialog import CrossCorrelationDialog
from ..dialogs.elemDetectSettings import ElemDetectSettingsDialog
from graphic_interface.windows.ToastWidget import ToastWidget
from sound_lab_core.Segmentation.SegmentManager import SegmentManager
from ..dialogs.ManualClassificationDialog import ManualClassificationDialog
from TwoDimensionalAnalisysWindow import TwoDimensionalAnalisysWindow
from ui_python_files.SegmentationAndClasificationWindowUI import Ui_MainWindow


class SegmentationClassificationWindow(SoundLabWindow, Ui_MainWindow):
    """

    Window that process the segmentation and classification of a signal
    Contains a QSignalDetectorWidget that wrapper several functionality
    Allows to select the segmentation and classification settings,
    and parameter measurement for detected segments.
    Provides a table for visualization of segment and measures,
    A two dimensional window to graph two measured params. One for each axis.
    Options for selection and visualization of segments
    Provides options for save the parameters to excel.
    """

    # region CONSTANTS

    # different colors for the even and odds rows in the parameter table and segment colors.
    TABLE_ROW_COLOR_ODD = QColor(0, 0, 255, 150)
    TABLE_ROW_COLOR_EVEN = QColor(0, 255, 0, 150)

    # stylesheet to use on excel file saved
    EXCEL_STYLE_HEADER = xlwt.easyxf('font: name Times New Roman, color-index black, bold on, height 300')
    EXCEL_STYLE_BODY = xlwt.easyxf('font: name Times New Roman, color-index black, height 220', num_format_str='#,# # 0.00')
    EXCEL_STYLE_COPYRIGHT = xlwt.easyxf('font: name Arial, color-index pale_blue, height 250, italic on', num_format_str='# ,# # 0.00')

    # endregion

    # region Initialize

    def __init__(self, parent=None, signal=None, workspace=None):
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

        # the segmentation window do not allow to record a signal (for now...)
        self.actionRecord.setEnabled(False)

        # the object that handles the measuring of parameters and manage the segments
        self.segmentManager = SegmentManager()
        self.segmentManager.measurementsChanged.connect(self.update_parameter_table)
        self.segmentManager.measurementsFinished.connect(self.measurement_finished)
        self.segmentManager.detectionProgressChanged.connect(lambda x: self.windowProgressDetection.setValue(x * 0.9))
        self.segmentManager.segmentVisualItemAdded.connect(self.widget.add_parameter_visual_items)

        # the factory of adapters for parameters to supply to the ui window or segmentation dialog
        self.parameter_manager = MeasurementTemplate(signal=signal)

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
        self.widget.toolDataDetected.connect(self.update_status_bar)
        self.widget.elementClicked.connect(self.select_element)

        self.dockWidgetParameterTableOscilogram.setVisible(False)
        self.tableParameterOscilogram.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableParameterOscilogram.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableParameterOscilogram.setSortingEnabled(False)

        # add the context menu actions to the widget
        self.__addContextMenuActions()

        # create the progress bar that is showed while the detection is made
        self.windowProgressDetection = QProgressBar(self)
        self.set_progress_bar_visibility(False)

        # array of windows with two dimensional graphs
        self.two_dim_windows = []
        self._cross_correlation_windows = []

        if workspace is not None:
            self.load_workspace(workspace)

        self.show()

        self.try_restore_previous_session()

    def try_restore_previous_session(self):
        """
        Restore (if any) the previous session with this file.
        That means detected elements, measured parameters etc that are saved on the signal
        extra data.
        :return:
        """
        elements = self.widget.get_signal_segmentation_data()


        if len(elements) == 0:
            return

        buttons_box = QMessageBox.Yes | QMessageBox.No
        mbox = QMessageBox(QMessageBox.Question, self.tr(u"soundLab"),
                           self.tr(u"The file has segmentation data stored. Do you want to load it?"), buttons_box, self)
        result = mbox.exec_()

        if result == QMessageBox.Yes:
            for i, e in enumerate(elements):
                self.segmentManager.add_element(i, e[0], e[1])

            self.widget.elements = self.segmentManager.elements
            self.segmentManager.measure_parameters_and_classify()
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
                # parameters manipulation actions
                self.actionMeditions,
                self.actionView_Parameters,
                self.actionAddElement,
                separator2,

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

                # change tools actions
                self.actionZoom_Cursor,
                self.actionPointer_Cursor,
                self.actionRectangular_Cursor,
                separator3,

                # elements select/deselect
                self.actionDeselect_Elements,
                self.actionDelete_Selected_Elements,
                self.actionSelectedElement_Correlation,
                self.actionClassify,
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
                                    self.actionDeselect_Elements, self.actionAddElement,
                                    self.actionParameter_Measurement, sep]

        for act in segm_transf_actions_list:
            act.setActionGroup(segm_transf_actions)

        # endregion

        # add to the customizable sound lab toolbar first than the default actions
        # addActionGroup(actionGroup, name)
        self.toolBar.addActionGroup(segm_transf_actions, u"Segments and Parameters")

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
        wnd.elementsClassified.connect(lambda indexes_list, classification:
                                       self.segmentManager.set_manual_elements_classification(indexes_list,
                                                                                              classification))

        # load the workspace in the new two dimensional window
        if self.workSpace:
            wnd.load_workspace(self.workSpace)

        # if any previous windows was opened then update in the new one the selected element
        if len(self.two_dim_windows) > 0:
            wnd.select_element(self.two_dim_windows[0].selectedElementIndex)

        # add the new window to the current opened windows
        self.two_dim_windows.append(wnd)

    def clear_two_dim_windows(self):
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
        :return: True if successfully False otherwise
        """
        file_name = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save parameters as excel file"),
                                                        os.path.join(self.workSpace.lastOpenedFolder,
                                                                     str(self.widget.signalName) + ".xls"), "*.xls"))
        # save the data of table
        if not file_name:
            return False

        # if successfully selected the path save the excel book of data
        try:

            wb = xlwt.Workbook()
            ws = wb.add_sheet("Elements Measurements")
            self.write_data(ws, self.tableParameterOscilogram)
            wb.save(file_name)

            self.segmentManager.save_data_on_db()

        except Exception as ex:
            print("Error saving the excel file. " + ex.message)

        return True

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

    def set_signal_file(self, file_path=''):
        """
        Update the data of the current signal file path origin in the widget
        (if any)
        :param file_path:
        :return:
        """
        self.widget.signalFilePath = file_path

    def write_data(self, ws, table_parameter):
        """
        Write the data from the table into an excel file stylesheet.
        :param ws:WorkSheet object from xwlt module for interacts with excell files.
        :param table_parameter: QTableWidget with the information of the data to save.
        """
        # write headers into the document
        headers = [str(table_parameter.takeHorizontalHeaderItem(pos).text()) for pos in
                   xrange(table_parameter.columnCount())]

        for index, header in enumerate(headers):
            ws.write(0, index, header, self.EXCEL_STYLE_HEADER)

        # write data into the document
        for i in xrange(1, table_parameter.model().rowCount() + 1):
            for j in xrange(table_parameter.model().columnCount()):
                cell_data = str(table_parameter.item(i - 1, j).data(Qt.DisplayRole).toString())

                ws.write(i, j, cell_data, self.EXCEL_STYLE_BODY)

        # ws object must be part of a Work book that would be saved later
        ws.write(table_parameter.model().rowCount() + 3, 0,
                 unicode(self.tr(u"duetto-Sound Lab")), self.EXCEL_STYLE_COPYRIGHT)

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

        mbox = QMessageBox(QMessageBox.Question, self.tr(u"Save measurements"),
                           self.tr(u"Do you want to save the parameters of " + unicode(self.widget.signalName)),
                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, self)

        # if the signal was playing must be stopped
        self.widget.stop()
        self.segmentManager.stop_processing()

        # if there is a measurement made and parameters measured that could be saved
        if self.tableParameterOscilogram.rowCount() > 0:

            result = mbox.exec_()

            # check if the user decision about save is discard and continue working
            if result == QMessageBox.Cancel or (result == QMessageBox.Yes and not self.on_actionMeditions_triggered()):
                event.ignore()
                return

            self.clear_two_dim_windows()

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
        deleted_elements = self.widget.selected_elements_interval()

        self.widget.delete_selected_elements()

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
    def on_actionDelete_All_triggered(self):
        """
        Removes all the detected elements on the widget
        :return:
        """
        # clear the segments
        self.segmentManager.elements = []

        # removes the widget elements
        self.widget.elements = []
        self.widget.graph()

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

        element = self.widget.get_element(element_added_index)

        self.segmentManager.add_element(element_added_index, element.indexFrom, element.indexTo)

        self.update_two_dim_windows()

        self.widget.graph()

        self.__set_parameter_window_visible()

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
        # select the element in the table of parameters
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

        # show the image if the element is classified
        try:
            classification = self.segmentManager.get_segment_classification(element_index)
            image = classification.get_image()
            if image:
                self.show_image_on_element(element_index, image)

            self.update_status_bar(classification.get_full_description())

        except Exception as ex:
            pass

    @pyqtSlot()
    def on_actionSelectedElement_Correlation_triggered(self):
        signal = self.widget.selected_element_signal()
        if not signal:
            QMessageBox.warning(QMessageBox(), self.tr(u"Error"), self.tr(u"There is no selected element."))
            return

        dialog = CrossCorrelationDialog(self, self.widget, signal, self.TABLE_ROW_COLOR_ODD, self.TABLE_ROW_COLOR_EVEN)

        self._cross_correlation_windows.append(dialog)
        dialog.elementSelected.connect(self.select_element)
        dialog.show()

    @pyqtSlot()
    def on_actionClassify_triggered(self):
        """
        Open the classification dialog for update the categories and values
        in which could be classified a segment.
        """
        # create and open the dialog to edit the classification categories
        selection = self.widget.selected_elements_interval()

        if selection is None:
            QMessageBox.warning(QMessageBox(), self.tr(u"Warning"), self.tr(u"There is no selection made."))
            return

        index_from, index_to = selection
        classification_dialog = ManualClassificationDialog()

        if classification_dialog.exec_():
            classification = classification_dialog.get_classification()
            self.segmentManager.set_manual_elements_classification(xrange(index_from, index_to + 1), classification)

    # endregion

    # region Classification

    def show_image_on_element(self, element_index, image):
        """
        show a toast with the specie image (if any and if is identified) of
        the element at element index position
        :param element_index:
        :return:
        """
        toast = ToastWidget(self, back_image=image, width=100, heigth=100)

        element = self.segmentManager.elements[element_index]
        min_x, max_x = self.widget.get_visible_region()

        x = element.indexFrom - min_x + (element.indexTo - element.indexFrom) / 2.0
        x = x * self.widget.width() * 1.0 / (max_x - min_x)

        toast.move(self.widget.mapToGlobal(QPoint(x - toast.width() / 2.0,
                   (self.widget.height() - toast.height()) / 2.0)))

        toast.disappear()

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

    # endregion

    # region Detection

    def set_progress_bar_visibility(self, visibility=True):
        """
        Show the progress bar in the middle of the widget.
        Used when a high time demanding task is going to be made to
        show to the user it's progress.
        :return:
        """
        if not visibility:
            self.windowProgressDetection.setVisible(False)

        else:
            width, height = self.width(), self.height()
            x, y = self.widget.x(), self.widget.y()
            progress_bar_height = height / 20.0

            self.windowProgressDetection.resize(width / 3.0, progress_bar_height)
            self.windowProgressDetection.move(x + width / 3.0, y + height / 2.0 + progress_bar_height / 2.0)
            self.windowProgressDetection.setVisible(True)

        self.repaint()

    @pyqtSlot()
    def on_actionDetection_triggered(self):
        """
        Method that execute the detection
        """

        # there is an on going detection been made
        if self.windowProgressDetection.isVisible():
            QMessageBox.warning(QMessageBox(), self.tr(u"Error"), self.tr(u"There is an on going detection in progress."))
            return

        elementsDetectorDialog = ElemDetectSettingsDialog(self, self.widget.signal, self.segmentManager)
        elementsDetectorDialog.modifyParametersMeasurement.connect(lambda: self.on_actionParameter_Measurement_triggered())
        elementsDetectorDialog.load_workspace(self.workSpace)

        try:
            if elementsDetectorDialog.exec_():
                # the detection dialog is a factory of segmentation,
                # parameter parameters and classification concrete implementations

                # get the segmentation, classification and parameters methods
                self.segmentManager.detector_adapter = elementsDetectorDialog.detector
                self.segmentManager.classifier_adapter = elementsDetectorDialog.classifier
                self.segmentManager.parameters = self.parameter_manager.parameter_list()

                self.windowProgressDetection.setValue(0)
                self.set_progress_bar_visibility(True)

                # execute the detection
                self.segmentManager.segmentationFinished.connect(self.segmentation_finished)
                self.segmentManager.detect_elements()

        except Exception as e:
            print("detection errors: " + e.message)

            self.windowProgressDetection.setValue(100)
            self.set_progress_bar_visibility(False)

    def segmentation_finished(self):
        """
        Callback to execute when the segmentation segmentation_thread finished.
        :return:
        """
        self.windowProgressDetection.setValue(90)

        # put the elements detected into the widget to visualize them
        self.widget.elements = self.segmentManager.elements
        self.widget.graph()

        self.windowProgressDetection.setValue(100)
        self.set_progress_bar_visibility(False)

        # measure the parameters over elements detected
        QTimer.singleShot(50, self.segmentManager.measure_parameters_and_classify)

    def measurement_finished(self):
        """
        Callback to execute when the measurement has finished.
        :return:
        """
        # must be refreshed the widget because the parameter measurement
        # may include visual items into the graph
        self.widget.graph()
        self.update_two_dim_windows()

        self.__set_parameter_window_visible()

    def __set_parameter_window_visible(self):

        # set the parameter window to visible state after measurements
        if not self.tableParameterOscilogram.isVisible():
            self.actionView_Parameters.setChecked(True)
            self.dockWidgetParameterTableOscilogram.setVisible(True)

    def update_two_dim_windows(self):
        # update the measured data on the two dimensional opened windows
        for wnd in self.two_dim_windows:
            wnd.load_data(self.segmentManager)

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

        self.widget.visual_items_visibility.oscilogram_items_visible = visibility
        self.widget.graph()

        for x in [self.actionTemporal_Figures, self.actionTemporal_Numbers, self.actionTemporal_Parameters]:
            x.setEnabled(visibility)

    @pyqtSlot()
    def on_actionTemporal_Figures_triggered(self):
        self.widget.visual_items_visibility.oscilogram_figures_visible = self.actionTemporal_Figures.isChecked()
        self.widget.graph()

    @pyqtSlot()
    def on_actionTemporal_Parameters_triggered(self):
        self.widget.visual_items_visibility.oscilogram_parameters_visible = self.actionTemporal_Parameters.isChecked()
        self.widget.graph()

    @pyqtSlot()
    def on_actionTemporal_Numbers_triggered(self):
        """
        Change visibility of the numbers of the detected segments on the oscilogram graph

        """
        self.widget.visual_items_visibility.oscilogram_text_visible = self.actionTemporal_Numbers.isChecked()
        self.widget.graph()

    @pyqtSlot()
    def on_actionSpectral_Elements_triggered(self):
        """
        Spectral Elements are the elements that are visible on the spectrogram graph.
        This method allows to change its visibility
        """
        visibility = self.actionSpectral_Elements.isChecked()

        self.widget.visual_items_visibility.spectrogram_items_visible = visibility
        self.widget.graph()

        for x in [self.actionSpectral_Numbers, self.actionSpectral_Figures, self.actionSpectral_Parameters]:
            x.setEnabled(visibility)

    @pyqtSlot()
    def on_actionSpectral_Figures_triggered(self):
        self.widget.visual_items_visibility.spectrogram_figures_visible = self.actionSpectral_Figures.isChecked()
        self.widget.graph()

    @pyqtSlot()
    def on_actionSpectral_Parameters_triggered(self):
        self.widget.visual_items_visibility.spectrogram_parameters_visible = self.actionSpectral_Parameters.isChecked()
        self.widget.graph()

    @pyqtSlot()
    def on_actionSpectral_Numbers_triggered(self):
        """
        Change visibility of the numbers of the detected segments on the oscilogram graph

        """
        self.widget.visual_items_visibility.spectrogram_text_visible = self.actionSpectral_Numbers.isChecked()
        self.widget.graph()

    # endregion

    def update_parameters(self, parameter_manager):
        """
        Updates the parameters to measure from a change in their selection.
        :param parameter_manager:
        :return:
        """
        # update the segment manager
        self.segmentManager.parameters = parameter_manager.parameter_list()

        self.update_two_dim_windows()

    @pyqtSlot()
    def on_actionParameter_Measurement_triggered(self):

        # check for previously parameters measurements to save
        # there is measured parameters when the list of their names has at least one element
        if len(self.segmentManager.parameterColumnNames) > 0:

            mbox = QMessageBox(QMessageBox.Question, self.tr(u"soundLab"),
                               self.tr(u"You are going to change the parameters to measure."
                                       u"All your previously selected measurements will be lost."
                                       u"Do you want to save measurements first?"), QMessageBox.Yes | QMessageBox.No, self)

            if mbox.exec_() == QMessageBox.Yes:
                self.on_actionMeditions_triggered()


        param_window = ParametersWindow(self, self.parameter_manager,
                                        self.widget.signal, workspace=self.workSpace)

        param_window.parameterChangeFinished.connect(lambda p: self.update_parameters(p))

        param_window.show()

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