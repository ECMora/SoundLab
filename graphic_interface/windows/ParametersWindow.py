#  -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QAbstractItemView
from pyqtgraph.parametertree import Parameter, ParameterTree
from sound_lab_core.ParametersMeasurement.Adapters.FreqParametersadapters.FreqParameterAdapter import \
    SpectralParameterAdapter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.LocationAdapter import LocationAdapter
from sound_lab_core.ParametersMeasurement.ParameterManager import ParameterManager
from ui_python_files.ParametersWindow import Ui_Dialog


class ParametersWindow(QtGui.QDialog, Ui_Dialog):
    """
    Window that visualize a parameter manager to change its configurations.
    Contains a tab widget with all the types of parameters to measure.
    """

    # SIGNALS
    # signal raised when the window has finished to interact with parameters
    parameterChangeFinished = pyqtSignal(object)

    def __init__(self, parent=None, parameter_manager=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        # configuration of parameters and location trees user interface
        self.parameter_tree_widget = ParameterTree()
        self.parameter_tree_widget.setAutoScroll(True)
        self.parameter_tree_widget.setHeaderHidden(True)

        self.location_tree_widget = ParameterTree()
        self.location_tree_widget.setAutoScroll(True)
        self.location_tree_widget.setHeaderHidden(True)

        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self.parameter_tree_widget)
        layout.addWidget(self.location_tree_widget)
        self.settings_widget.setLayout(layout)

        self.param_measurement_tree = None
        self.location_measurement_tree = None

        # create the parameter trees for parameter settings and location settings
        self.param_measurement_tree = Parameter.create(name=unicode(self.tr(u'Parameter Settings')), type=u'group')
        self.parameter_tree_widget.setParameters(self.param_measurement_tree)

        self.location_measurement_tree = Parameter.create(name=unicode(self.tr(u'Location Settings')), type=u'group')
        self.location_tree_widget.setParameters(self.location_measurement_tree)

        # tables are just for selection (of parameter-location) not for edit elements.
        self.parameter_locations_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.wave_parameter_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.time_parameter_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self._parameter_manager = None
        self.parameter_manager = parameter_manager if parameter_manager is not None else ParameterManager()

        # if accepted or cancel anyway raise the changes
        self.buttonBox.clicked.connect(lambda bttn: self.parameterChangeFinished.emit(self.parameter_manager))

    # region Properties

    @property
    def parameter_manager(self):
        return self._parameter_manager

    @parameter_manager.setter
    def parameter_manager(self, parameter):
        self._parameter_manager = parameter

        # when change the parameter manager updates its values on the tables
        self.load_parameters()

    # endregion

    # region Load Parameters

    def load_parameters(self):
        """
        Updates the parameter configuration on the window with the ones in the parameter manager.
        parameter_manager.
        :return:
        """

        if self.parameter_manager is None:
            return

        self.load_time_based_parameters()

        table = self.wave_parameter_table
        adapters = self.parameter_manager.wave_parameters_adapters
        locations_adapters = self.parameter_manager.wave_locations_adapters
        self.load_parameters_locations(table, locations_adapters, adapters, self.parameter_manager.wave_location_parameters)

        table = self.parameter_locations_table
        locations_adapters = self.parameter_manager.spectral_time_locations_adapters
        adapters = self.parameter_manager.spectral_parameters_adapters
        self.load_parameters_locations(table, locations_adapters, adapters, self.parameter_manager.spectral_location_parameters)

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

        adapters = self.parameter_manager.time_parameters_adapters

        # first row for the 'select all' option
        table.setRowCount(1 + len(adapters))
        table.setVerticalHeaderLabels([self.tr(u"Select All")] + [x.name for x in adapters])

        table.setColumnCount(1)
        table.setHorizontalHeaderLabels([self.tr(u"Measure")])
        all_selected = True

        # the first row (0 index) is for the select all option
        for i in xrange(table.rowCount()):
            item = QtGui.QTableWidgetItem("")

            state = Qt.Unchecked if i == 0 or not self.parameter_manager.time_location_parameters[i-1] else Qt.Checked

            all_selected = all_selected and (i == 0 or state == Qt.Checked)

            item.setCheckState(state)

            table.setItem(i, 0, item)

        if all_selected:
            table.item(0, 0).setCheckState(Qt.Checked)

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

        table.cellClicked.connect(lambda x, y: self.parameter_spectral_selected(table, x, y, param_adapters,
                                                                                selection_matrix, time_locations_adapters))
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    # endregion

    def parameter_spectral_selected(self, table, row, col, param_adapters, selection_matrix, time_locations_adapters=None):

        # select all params all locations
        if row == 0 and col == 0:
            # update the columns 'select all' values
            for i in xrange(1, table.columnCount()):
                table.item(row, i).setCheckState(table.item(row, col).checkState())

            for i in xrange(1, table.rowCount()):
                table.item(i, col).setCheckState(table.item(row, col).checkState())
                self.parameter_spectral_selected(table, i, col, param_adapters, selection_matrix, time_locations_adapters)

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
            self.update_parameter_and_locations_settings(row - 1, col - 1, param_adapters, time_locations_adapters)

    def parameter_time_selected(self, row, col, param_adapters):
        table = self.time_parameter_table if self.tab_time_parameters.isVisible() else self.wave_parameter_table

        if row == 0:
            for i in xrange(1, table.rowCount()):
                table.item(i, col).setCheckState(table.item(row, col).checkState())

            self.parameter_manager.time_location_parameters[:] = table.item(row, col).checkState() == Qt.Checked
            return

        self.parameter_manager.time_location_parameters[row - 1] = table.item(row, col).checkState() == Qt.Checked
        self.update_parameter_and_locations_settings(row - 1, col, param_adapters, self.parameter_manager.time_location_parameters)

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

            if isinstance(time_locations_adapters, LocationAdapter):
                time_location_adapter = time_locations_adapters[col]
                location_settings = time_location_adapter.get_settings()
                self.location_measurement_tree.addChild(location_settings)

            if isinstance(parameter_adapter, SpectralParameterAdapter):
                spectral_location_adapter = self.parameter_manager.spectral_locations_adapters[row, col]
                spectral_location_settings = spectral_location_adapter.get_settings()
                self.location_measurement_tree.addChild(spectral_location_settings)

        except Exception as ex:
            print("updating settings " + ex.message)
