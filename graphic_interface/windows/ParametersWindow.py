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

        # create the parameter tree
        self.param_measurement_tree = Parameter.create(name=unicode(self.tr(u'Parameter Settings')), type=u'group')
        self.location_measurement_tree = Parameter.create(name=unicode(self.tr(u'Location Settings')), type=u'group')

        self.parameter_tree_widget.setParameters(self.param_measurement_tree)
        self.location_tree_widget.setParameters(self.location_measurement_tree)

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
        rows = [x.name for x in adapters]
        self.load_time_based_parameters(table, rows, adapters)

        table = self.wave_parameter_table
        adapters = self.parameter_manager.wave_parameters_adapters
        rows = [x.name for x in adapters]
        self.load_time_based_parameters(table, rows, adapters)

        self.load_spectral_parameters()

        # clear the parameter-location settings tree
        self.param_measurement_tree.clearChildren()
        self.location_measurement_tree.clearChildren()

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
        all_selected = True

        # load spectral params and locations
        # the first row (0 index) is for the select all option
        for i in xrange(table.rowCount()):
            item = QtGui.QTableWidgetItem("")

            state = Qt.Unchecked if (i == 0 or not adapters[i - 1].selected) else Qt.Checked
            all_selected = all_selected and (i == 0 or state == Qt.Checked)

            item.setCheckState(state)
            table.setItem(i, 0, item)

        if all_selected:
            table.item(0, 0).setCheckState(Qt.Checked)

        table.cellClicked.connect(lambda x, y: self.parameter_time_selected(x, y, adapters))

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

        row_names = [self.tr(u"All Params")] + [x.name for x in param_adapters]
        column_names = [self.tr(u"All Locations")] + [x.name for x in locations_adapters]

        # load spectral params and locations
        for i in xrange(table.rowCount()):
            for j in xrange(table.columnCount()):
                item = QtGui.QTableWidgetItem("")
                table.setItem(i, j, item)

                state = Qt.Unchecked
                if i > 0 and j > 0 and self.parameter_manager.location_parameters[i - 1, j - 1]:
                    state = Qt.Checked

                item.setCheckState(state)

        all_selected = True

        # set the state for the select all options items
        for i in xrange(1, table.rowCount()):
            state = Qt.Checked if self.parameter_manager.location_parameters[i - 1, :].all() else Qt.Unchecked
            table.item(i, 0).setCheckState(state)

        for i in xrange(1, table.columnCount()):
            state = Qt.Checked if self.parameter_manager.location_parameters[:, i - 1].all() else Qt.Unchecked
            table.item(0, i).setCheckState(state)
            all_selected = all_selected and (state == Qt.Checked)

        table.item(0, 0).setCheckState(Qt.Checked if all_selected else Qt.Unchecked)

        table.setVerticalHeaderLabels(row_names)
        table.setHorizontalHeaderLabels(column_names)

        table.cellClicked.connect(lambda x, y: self.parameter_spectral_selected(x, y, param_adapters, locations_adapters))
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    # endregion

    def parameter_spectral_selected(self, row, col, param_adapters, locations_adapters=None):

        table = self.parameter_locations_table

        # select all params all locations
        if row == 0 and col == 0:
            # update the columns 'select all' values
            for i in xrange(1, table.columnCount()):
                table.item(row, i).setCheckState(table.item(row, col).checkState())

            for i in xrange(1, table.rowCount()):
                table.item(i, col).setCheckState(table.item(row, col).checkState())
                self.parameter_spectral_selected(i, col, param_adapters, locations_adapters)

        elif row == 0:
            for i in xrange(1, table.rowCount()):
                table.item(i, col).setCheckState(table.item(row, col).checkState())
                self.parameter_manager.location_parameters[i - 1, col] = table.item(row, col).checkState() == Qt.Checked

        elif col == 0:
            for i in xrange(1, table.columnCount()):
                table.item(row, i).setCheckState(table.item(row, col).checkState())
                self.parameter_manager.location_parameters[row - 1, i - 1] = table.item(row, col).checkState() == Qt.Checked
        else:
            self.parameter_manager.location_parameters[row - 1, col - 1] = table.item(row, col).checkState() == Qt.Checked
            self.update_parameter_and_locations_settings(row - 1, col - 1, param_adapters, locations_adapters)

    def parameter_time_selected(self, row, col, param_adapters):
        table = self.time_parameter_table if self.tab_time_parameters.isVisible() else self.wave_parameter_table

        if row == 0:
            for i in xrange(1, table.rowCount()):
                table.item(i, col).setCheckState(table.item(row, col).checkState())
                param_adapters[i - 1].selected = table.item(row, col).checkState() == Qt.Checked
            return

        param_adapters[row-1].selected = table.item(row, col).checkState() == Qt.Checked
        self.update_parameter_and_locations_settings(row - 1, col, param_adapters)

    def update_parameter_and_locations_settings(self, row, col, param_adapters, locations_adapters=None):
        # update tree of parameter settings and locations
        self.param_measurement_tree.clearChildren()
        self.location_measurement_tree.clearChildren()

        try:
            parameter_adapter = param_adapters[row]
            param_settings = parameter_adapter.get_settings()
            self.param_measurement_tree.addChild(param_settings)

        except Exception as ex:
            print("updating settings " + ex.message)

        try:
            location_adapter = locations_adapters[col]
            location_settings = location_adapter.get_settings()
            self.location_measurement_tree.addChild(location_settings)

        except Exception as ex:
            print("updating settings " + ex.message)