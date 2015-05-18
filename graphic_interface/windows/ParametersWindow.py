#  -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QAbstractItemView
from pyqtgraph.parametertree import Parameter, ParameterTree
from sound_lab_core.ParametersMeasurement.ParameterManager import ParameterManager
from ui_python_files.ParametersWindow import Ui_Dialog


class ParametersWindow(QtGui.QDialog, Ui_Dialog):
    """
    Window that visualize a parameter manager to change its configurations.
    Contains a tab widget with all the types of parameters to measure.
    """

    def __init__(self, parent=None, parameter_manager=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

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

        self.parameters = []

        self.parameter_locations_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.wave_parameter_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.time_parameter_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self._parameter_manager = None
        self.parameter_manager = parameter_manager if parameter_manager is not None else ParameterManager()

    # region Properties

    @property
    def parameter_manager(self):
        return self._parameter_manager

    @parameter_manager.setter
    def parameter_manager(self, parameter):
        self._parameter_manager = parameter

        # update table if parameter changes
        self.load_parameters()

    # endregion

    # region Load Parameters

    def load_parameters(self):
        """
        Load into the window the parameter configuration on its
        parameter_manager.
        :return:
        """
        if self.parameter_manager is None:
            return

        table = self.time_parameter_table
        adapters = self.parameter_manager.time_parameters_adapters
        rows = [x[0] for x in adapters]
        self.load_time_based_parameters(table, rows, adapters)

        table = self.wave_parameter_table
        adapters = self.parameter_manager.wave_parameters_adapters
        rows = [x[0] for x in adapters]
        self.load_time_based_parameters(table, rows, adapters)

        self.load_spectral_parameters()

        self.create_settings_tree()

    def load_time_based_parameters(self, table, row_names, adapters):
        """
        Load into the supplied table widget the data to use the adapters.
        :param table: The table in which will be loaded the parameters.
        :param row_names: the name of the rows in the table
        :param adapters: the adapters dor each parameter (same length of rows_names)
        :return:
        """
        # first row for the 'select all' option
        table.setRowCount(1 + len(adapters))
        table.setVerticalHeaderLabels([self.tr(u"Select All")] + row_names)

        table.setColumnCount(1)
        table.setHorizontalHeaderLabels([self.tr(u"Measure")])

        # load spectral params and locations
        for i in xrange(table.rowCount()):
            item = QtGui.QTableWidgetItem("")
            item.setCheckState(Qt.Unchecked)
            table.setItem(i, 0, item)

        table.cellClicked.connect(lambda x, y: self.parameter_selected(x, y, adapters))

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    def load_spectral_parameters(self):
        """
        Load into the spectral tab widget the data of the current parameter manager
        :return:
        """
        table = self.parameter_locations_table
        locations_adapters = self.parameter_manager.locations_adapters
        param_adapters = self.parameter_manager.spectral_parameters_adapters

        # one extra row and column for the 'select all' option
        table.setRowCount(1 + len(param_adapters))
        table.setColumnCount(1 + len(locations_adapters))

        row_names = [self.tr(u"All Params")] + [x[0] for x in param_adapters]
        column_names = [self.tr(u"All Locations")] + [x[0] for x in locations_adapters]

        # load spectral params and locations
        for i in xrange(table.rowCount()):
            for j in xrange(table.columnCount()):
                item = QtGui.QTableWidgetItem("")
                table.setItem(i, j, item)

                # the 0,0 is the ['All Locations','All Params'] cell
                if i == 0 and j == 0:
                    continue

                item.setCheckState(Qt.Unchecked)

        table.setVerticalHeaderLabels(row_names)
        table.setHorizontalHeaderLabels(column_names)

        table.cellClicked.connect(lambda x, y: self.parameter_selected(x, y, param_adapters,
                                                                       locations_adapters))
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    # endregion

    def create_settings_tree(self):
        # set the segmentation and classification parameters
        self.param_measurement_tree = Parameter.create(name=unicode(self.tr(u'Parameter Settings')), type=u'group')
        self.location_measurement_tree = Parameter.create(name=unicode(self.tr(u'Location Settings')), type=u'group')

        self.parameter_tree_widget.setParameters(self.param_measurement_tree)
        self.location_tree_widget.setParameters(self.location_measurement_tree)

    def parameter_selected(self, row, col, param_adapters, locations_adapters=None):

        if self.tab_spectral_params.isVisible():
            table = self.parameter_locations_table

        elif self.tab_time_parameters.isVisible():
            table = self.time_parameter_table

        elif self.tab_wave_parameters.isVisible():
            table = self.wave_parameter_table

        if row == 0:
            for i in xrange(1, table.rowCount()):
                table.item(i, col).setCheckState(table.item(row, col).checkState())
            return

        if table == self.parameter_locations_table and col == 0:
            for i in xrange(1, table.columnCount()):
                table.item(row, i).setCheckState(table.item(row, col).checkState())
            return

        update_col = col - 1 if table == self.parameter_locations_table else col

        self.update_parameter_and_locations_settings(row - 1, update_col, param_adapters, locations_adapters)

    def update_parameter_and_locations_settings(self, row, col, param_adapters, locations_adapters=None):
        # update tree of parameter settings and locations
        self.param_measurement_tree.clearChildren()
        self.location_measurement_tree.clearChildren()

        try:
            parameter_adapter = param_adapters[row]
            param_settings = parameter_adapter[1].get_settings()
            self.param_measurement_tree.addChild(param_settings)

        except Exception as ex:
            print("updating settings " + ex.message)

        try:
            location_adapter = locations_adapters[col]
            location_settings = location_adapter[1].get_settings()
            self.location_measurement_tree.addChild(location_settings)

        except Exception as ex:
            print("updating settings " + ex.message)

    def get_parameter_list(self):
        """
        :return: The list of parameters to measure
        """
        time_based_parameters = []
        for x in xrange(2):
            table = [self.time_parameter_table, self.wave_parameter_table][x]
            parameter_adapter = [self.parameter_manager.time_parameters_adapters,
                                 self.parameter_manager.wave_parameters_adapters][x]

            for i in xrange(1, table.rowCount()):
                if table.item(i, 0).checkState() == Qt.Checked:
                    parameter = parameter_adapter[i - 1][1].get_instance()
                    time_based_parameters.append(parameter)

        spectral_parameters = []
        table = self.parameter_locations_table
        for i in xrange(1, table.rowCount()):
            for j in xrange(1, table.columnCount()):
                if table.item(i, j).checkState() == Qt.Checked:
                    parameter = self.parameter_manager.spectral_parameters_adapters[i - 1][1].get_instance()
                    parameter.location = self.parameter_manager.locations_adapters[j - 1][1].get_instance()
                    spectral_parameters.append(parameter)

        return time_based_parameters + spectral_parameters

    def closeEvent(self, *args, **kwargs):
        self.parameter_manager.parameter_list = self.get_parameter_list()

        self.parameters = self.parameter_manager.parameter_list

        QtGui.QDialog.closeEvent(self, *args, **kwargs)