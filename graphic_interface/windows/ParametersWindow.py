#  -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui
from utils.Utils import small_signal
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QAbstractItemView
from duetto.audio_signals import openSignal
from ui_python_files.ParametersWindow import Ui_Dialog
from pyqtgraph.parametertree import Parameter, ParameterTree
from utils.Utils import folder_files, serialize, deserialize
from graphic_interface.widgets.signal_visualizer_tools import Tools
from sound_lab_core.Segmentation.SegmentManager import SegmentManager
from sound_lab_core.ParametersMeasurement.MeasurementTemplate import MeasurementTemplate


class ParametersWindow(QtGui.QDialog, Ui_Dialog):
    """
    Window that visualize a parameter manager to change its configurations.
    Contains a tab widget with all the types of parameters to measure.
    """

    # region CONSTANTS

    MEASUREMENT_TEMPLATE_FOLDER = os.path.join("utils", "measurement_templates")

    PARAMETER_VISUALIZATION_SIGNAL_PATH = os.path.join(os.path.join("utils", "measurement_templates"),
                                                       "measurement_params_example.wav")

    # endregion

    # region SIGNALS

    # signal raised when the window has finished to interact with parameters
    parameterChangeFinished = pyqtSignal(object)

    # endregion

    # region Initialize

    def __init__(self, parent=None, measurement_template=None, signal=None, workspace=None):
        """
        :type specgram_data: dict with the options of spectrogram creation on main window
        options are NFFT and overlap
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        # the list of templates names
        self.templates_paths = []
        self.load_templates()

        # if accepted or cancel anyway raise the changes
        self.buttonBox.clicked.connect(lambda bttn: self.parameterChangeFinished.emit(self.measurement_template))

        self.remove_measurement_template_bttn.clicked.connect(self.delete_template)
        self.save_measurement_template_as_bttn.clicked.connect(self.save_template_as)
        self.measurement_template_cbox.currentIndexChanged.connect(self.select_template)

        # configuration of parameters and location trees user interface
        self.parameter_tree_widget = ParameterTree()
        self.parameter_tree_widget.setAutoScroll(True)
        self.parameter_tree_widget.setHeaderHidden(True)

        self.location_tree_widget = ParameterTree()
        self.location_tree_widget.setAutoScroll(True)
        self.location_tree_widget.setHeaderHidden(True)

        # create and set the layout for the parameter and location settings widget
        self.create_layout_for_settings_widget()

        self.param_measurement_tree = None
        self.location_measurement_tree = None

        # create the parameter trees for parameter settings and location settings
        self.param_measurement_tree = Parameter.create(name=unicode(self.tr(u'Parameter')), type=u'group')
        self.parameter_tree_widget.setParameters(self.param_measurement_tree)

        self.location_measurement_tree = Parameter.create(name=unicode(self.tr(u'Location')), type=u'group')
        self.location_tree_widget.setParameters(self.location_measurement_tree)

        # tables are just for selection (of parameter-location) not for edit elements.
        self.parameter_locations_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.wave_parameter_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.time_parameter_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.workspace = workspace
        self.signal = signal

        self._measurement_template = None
        self.measurement_template = measurement_template if measurement_template is not None else MeasurementTemplate()

        # pre visualization signal
        try:
            signal = openSignal(self.PARAMETER_VISUALIZATION_SIGNAL_PATH)

        except Exception as e:
            signal = small_signal(signal)

        self.configure_advanced_mode_items(signal)

        self.segmentManager = SegmentManager()

        self.segmentManager.signal = self.widget.signal
        self.segmentManager.segmentVisualItemAdded.connect(self.widget.add_parameter_visual_items)
        self.segmentManager.measurementsChanged.connect(self.widget.draw_elements)
        self.try_load_signal_segment()

    def configure_advanced_mode_items(self, signal):
        """
        Configure the setting of the advanced mode window.
        :param signal: the signal to graph with the segment to dynamically
        measure the parameters and display items
        :return:
        """
        self.widget.signal = signal
        self.widget.visibleSpectrogram = True
        self.widget.visibleOscilogram = False

        if self.workspace is not None:
            self.widget.load_workspace(self.workspace)

        self.visible_oscilogram_cbox.stateChanged.connect(self.update_widget_graphs_visibility)
        self.visible_spectrogram_cbox.stateChanged.connect(self.update_widget_graphs_visibility)
        self.visible_spectrogram_cbox.setChecked(True)
        self.visible_oscilogram_cbox.setChecked(False)
        self.widget.setSelectedTool(Tools.NoTool)

        def visibility_function():
            visibility = self.advanced_mode_visibility_cbox.isChecked()
            self.dock_widget_advanced_mode.setVisible(visibility)
            if visibility:
                self.update_parameter_pre_visualization()

        self.advanced_mode_visibility_cbox.stateChanged.connect(visibility_function)
        self.dock_widget_advanced_mode.setVisible(False)
        self.finished.connect(lambda _: self.dock_widget_advanced_mode.setVisible(False))

    def create_layout_for_settings_widget(self):
        label = QtGui.QLabel("<center><h4>" + self.tr(u"Settings") + "</h4></center>")
        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(label)
        layout.addWidget(self.parameter_tree_widget)
        layout.addWidget(self.location_tree_widget)
        self.settings_widget.setLayout(layout)

    def try_load_signal_segment(self):
        """
        Restore (if any) the previous session with this file.
        That means detected elements, measured parameters etc that are saved on the signal
        extra data.
        :return:
        """
        segments = self.widget.get_signal_segmentation_data()

        if len(segments) == 0:
            return

        for i, e in enumerate(segments):
            self.segmentManager.add_element(i, e[0], e[1])

        self.widget.elements = self.segmentManager.elements
        self.widget.graph()

    def update_widget_graphs_visibility(self):
        osc_visibility = self.visible_oscilogram_cbox.isChecked()
        spec_visibility = self.visible_spectrogram_cbox.isChecked()

        if self.widget.visibleOscilogram != osc_visibility:
            self.widget.visibleOscilogram = osc_visibility

        if self.widget.visibleSpectrogram != spec_visibility:
            self.widget.visibleSpectrogram = spec_visibility

        self.widget.setVisible(osc_visibility or spec_visibility)

        self.widget.graph()

    # endregion

    # region Measurement Template Actions

    def select_template(self, index):
        """
        Select the template at index supplied.
        :param index:
        :return:
        """
        if index == 0:
            # the --new-- or blank measurement template
            self.measurement_template = MeasurementTemplate()
            return

        try:
            self.measurement_template.load_state(deserialize(self.templates_paths[index-1]))
            self.load_parameters()
            self.update_parameter_pre_visualization()

        except Exception as e:
            print(e.message)
            self.select_template(0)

    def load_templates(self):
        """
        Load all the available templates from disc
        (if any) and fills the combo box with them.
        :return:
        """
        self.measurement_template_cbox.clear()

        # the 0 index of the combo has the new template option for unsaved ones
        self.measurement_template_cbox.addItem("--new--")

        self.templates_paths = folder_files(self.MEASUREMENT_TEMPLATE_FOLDER, extensions=[".dmt"])

        templates = []

        for path in self.templates_paths:
            try:
                templates.append(deserialize(path)["name"])

            except Exception as e:
                templates.append(path)

        self.measurement_template_cbox.addItems(templates)

    def save_template_as(self):
        """
        Save the current template as a new one in the system.
        :return:
        """
        new_template_name = unicode(self.new_template_name_linedit.text())
        template_names = [unicode(self.measurement_template_cbox.itemText(i))
                          for i in range(self.measurement_template_cbox.count())]

        if not new_template_name:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"),
                                      self.tr(u"You have to write a name for the measurement template."))
            return

        elif new_template_name in template_names:
            error_msg = self.tr(u"There is already a template with that name.")
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"), error_msg)
            return

        # save the template as new one
        self.measurement_template.name = new_template_name

        try:
            new_template_path = os.path.join(self.MEASUREMENT_TEMPLATE_FOLDER,
                                             self.measurement_template.name + ".dmt")

            serialize(new_template_path, self.measurement_template.get_state())

            self.templates_paths.append(new_template_path)
            self.measurement_template_cbox.addItem(new_template_name)

            # the first index is for the --new-- template
            self.measurement_template_cbox.setCurrentIndex(len(self.templates_paths))

        except Exception as e:
            print e.message
            error_msg = self.tr(u"An error occurs when the template was been saved. Try it again")
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"), error_msg)

    def delete_template(self):
        """
        removes (if possible) the current template from the list of templates.
        :return:
        """

        text = self.tr(u"The current measurement template is protected and could not be deleted.")

        if not self.measurement_template.editable:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Error"), text)
            return

        current_template_index = self.measurement_template_cbox.currentIndex()

        if current_template_index == 0:
            return

        # delete the file
        try:
            os.remove(os.path.join(self.MEASUREMENT_TEMPLATE_FOLDER,
                                   self.measurement_template.name + ".dmt"))

            self.measurement_template_cbox.removeItem(current_template_index)
            del self.templates_paths[current_template_index - 1]

        except Exception as e:
            pass

        # select the --new-- template at 0 index in the combo box
        self.measurement_template_cbox.setCurrentIndex(0)

    # endregion

    # region Properties

    @property
    def measurement_template(self):
        return self._measurement_template

    @measurement_template.setter
    def measurement_template(self, parameter):
        if not isinstance(parameter, MeasurementTemplate):
            raise Exception("Invalid type of argument. Must be of type MeasurementTemplate")

        self._measurement_template = parameter
        self.config_measurement_template()

        for adapter in self.measurement_template.get_data_changing_adapters():
            adapter.dataChanged.connect(self.update_parameter_pre_visualization)

        # when change the parameter manager updates its values on the tables
        self.load_parameters()
    # endregion

    # region Load Parameters

    def config_measurement_template(self):
        """
        sets the configuration if any of the values in the measurement template
        accord to the current signal in process by the system
        :return:
        """

        if self.signal is not None:
            self.measurement_template.update_adapters_data(self.signal)

        if self.workspace is not None:
            NFFT = self.workspace.spectrogramWorkspace.FFTSize
            overlap = self.workspace.spectrogramWorkspace.FFTOverlap

            # the overlap on the workspace is between 0 and 1
            # and is -1 if automatic overlap selected by system
            overlap = 50 if overlap < 0 else overlap * 100

            spectrogram_data = dict(NFFT=NFFT, overlap=overlap)
            self.measurement_template.update_locations_data(spectrogram_data)

    def load_parameters(self):
        """
        Updates the parameter configuration on the window with the ones in the parameter template.
        :return:
        """

        if self.measurement_template is None:
            return

        self.load_time_based_parameters()

        table = self.wave_parameter_table
        adapters = self.measurement_template.wave_parameters_adapters
        locations_adapters = self.measurement_template.wave_locations_adapters
        self.load_parameters_locations(table, locations_adapters, adapters, self.measurement_template.wave_location_parameters)

        table = self.parameter_locations_table
        locations_adapters = self.measurement_template.spectral_time_locations_adapters
        adapters = self.measurement_template.spectral_parameters_adapters
        self.load_parameters_locations(table, locations_adapters, adapters, self.measurement_template.spectral_location_parameters)

        # clear the parameter-location settings tree
        self.param_measurement_tree.clearChildren()
        self.location_measurement_tree.clearChildren()

    def load_time_based_parameters(self):
        """
        Load into the time parameter table widget the data of the time parameter adapters from the manager.
        :return:
        """

        # commodity variable for table
        table = self.time_parameter_table

        adapters = self.measurement_template.time_parameters_adapters

        # first row for the 'select all' option
        table.setRowCount(1 + len(adapters))
        table.setVerticalHeaderLabels([self.tr(u"Select All")] + [x.name for x in adapters])

        table.setColumnCount(1)
        table.setHorizontalHeaderLabels([self.tr(u"Measure")])
        all_selected = True

        # the first row (0 index) is for the select all option
        for i in xrange(table.rowCount()):
            item = QtGui.QTableWidgetItem("")

            state = Qt.Unchecked if i == 0 or not self.measurement_template.time_location_parameters[i-1] else Qt.Checked

            all_selected = all_selected and (i == 0 or state == Qt.Checked)

            item.setCheckState(state)

            table.setItem(i, 0, item)

        if all_selected:
            table.item(0, 0).setCheckState(Qt.Checked)

        def time_selection_function(row, col):
            state = Qt.Unchecked if table.item(row, col).checkState() == Qt.Checked else Qt.Checked
            table.item(row, col).setCheckState(state)

        table.cellPressed.connect(time_selection_function)
        table.cellClicked.connect(lambda row, col: self.parameter_time_selected(row, col, adapters))

        # fit the contents of the parameters names on the cells
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    def load_parameters_locations(self, table, time_locations_adapters, param_adapters, selection_matrix):
        """
        Load into the spectral tab widget the data of the current parameter manager
        :return:
        """
        # one extra row and column for the 'select all' option
        table.setRowCount(1 + len(param_adapters))
        table.setColumnCount(1 + len(time_locations_adapters))

        row_names = [self.tr(u"All Params")] + [x.name for x in param_adapters]
        column_names = [self.tr(u"All Locations")] + [x.name for x in time_locations_adapters]

        # load spectral params and locations
        for i in xrange(table.rowCount()):
            for j in xrange(table.columnCount()):
                item = QtGui.QTableWidgetItem("")
                table.setItem(i, j, item)

                state = Qt.Unchecked
                if i > 0 and j > 0 and selection_matrix[i - 1, j - 1]:
                    state = Qt.Checked

                item.setCheckState(state)

        all_selected = True

        # set the state for the select all options items
        for i in xrange(1, table.rowCount()):
            state = Qt.Checked if selection_matrix[i - 1, :].all() else Qt.Unchecked
            table.item(i, 0).setCheckState(state)

        for i in xrange(1, table.columnCount()):
            state = Qt.Checked if selection_matrix[:, i - 1].all() else Qt.Unchecked
            table.item(0, i).setCheckState(state)
            all_selected = all_selected and (state == Qt.Checked)

        table.item(0, 0).setCheckState(Qt.Checked if all_selected else Qt.Unchecked)

        table.setVerticalHeaderLabels(row_names)
        table.setHorizontalHeaderLabels(column_names)

        def selection_function(x, y):
            state = Qt.Unchecked if table.item(x, y).checkState() == Qt.Checked else Qt.Checked
            table.item(x, y).setCheckState(state)

        table.cellPressed.connect(selection_function)
        table.cellClicked.connect(lambda x, y:
                                  self.parameter_spectral_selected(table, x, y, param_adapters,
                                                                   selection_matrix, time_locations_adapters))

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    # endregion

    def parameter_spectral_selected(self, table, row, col, param_adapters, selection_matrix,
                                    time_locations_adapters=None, select_all_parameters=False):

        # select all params all locations
        if row == 0 and col == 0:
            # update the columns 'select all' values
            for i in xrange(1, table.columnCount()):
                table.item(row, i).setCheckState(table.item(row, col).checkState())

            for i in xrange(1, table.rowCount()):
                table.item(i, col).setCheckState(table.item(row, col).checkState())
                self.parameter_spectral_selected(table, i, col, param_adapters,
                                                 selection_matrix, time_locations_adapters, True)

        elif row == 0:
            for i in xrange(1, table.rowCount()):
                table.item(i, col).setCheckState(table.item(row, col).checkState())
                selection_matrix[i - 1, col - 1] = table.item(row, col).checkState() == Qt.Checked

        elif col == 0:
            for i in xrange(1, table.columnCount()):
                table.item(row, i).setCheckState(table.item(row, col).checkState())
                selection_matrix[row - 1, i - 1] = table.item(row, col).checkState() == Qt.Checked
        else:
            selection_matrix[row - 1, col - 1] = table.item(row, col).checkState() == Qt.Checked

            # boolean to avoid multiple computation with recursive calls
            if not select_all_parameters:
                self.update_parameter_and_locations_settings(row - 1, col - 1, param_adapters, time_locations_adapters)

        if not select_all_parameters:
            table.repaint()
            self.settings_widget.repaint()
            self.update_parameter_pre_visualization()

    def parameter_time_selected(self, row, col, param_adapters):

        table = self.time_parameter_table if self.tab_time_parameters.isVisible() else self.wave_parameter_table

        if row == 0:
            for i in xrange(1, table.rowCount()):
                table.item(i, col).setCheckState(table.item(row, col).checkState())

            self.measurement_template.time_location_parameters[:] = table.item(row, col).checkState() == Qt.Checked
            return

        self.measurement_template.time_location_parameters[row - 1] = table.item(row, col).checkState() == Qt.Checked
        self.update_parameter_and_locations_settings(row - 1, col,
                                                     param_adapters,
                                                     self.measurement_template.spectral_time_locations_adapters)

        # make a fast visible the change on the checkbox to prevent multiple clicks
        table.repaint()

        self.update_parameter_pre_visualization()

    def update_parameter_and_locations_settings(self, row, col, param_adapters, time_locations_adapters=None):
        # update tree of parameter settings and locations
        self.param_measurement_tree.clearChildren()
        self.location_measurement_tree.clearChildren()
        if row < 0 or col < 0:
            return

        try:
            parameter_adapter = param_adapters[row]
            param_settings = parameter_adapter.get_settings()
            self.param_measurement_tree.addChild(param_settings)

            if time_locations_adapters is not None:
                time_location_adapter = time_locations_adapters[col]
                location_settings = time_location_adapter.get_settings()
                self.location_measurement_tree.addChild(location_settings)

            # spectral locations reserved for future versions
            # if isinstance(parameter_adapter, SpectralParameterAdapter):
            #     spectral_location_adapter = self.measurement_template.spectral_locations_adapters[row, col]
            #     spectral_location_settings = spectral_location_adapter.get_settings()
            #     self.location_measurement_tree.addChild(spectral_location_settings)

        except Exception as ex:
            print("updating settings " + ex.message)

    def update_parameter_pre_visualization(self):
        if self.widget.visibleSpectrogram or self.widget.visibleOscilogram:
            self.segmentManager.parameters = self.measurement_template.parameter_list()

            self.widget.elements = self.segmentManager.elements

            self.segmentManager.measure_parameters_and_classify()

    def resizeEvent(self, event):
        QtGui.QDialog.resizeEvent(self, event)
        self.widget.graph()