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

        # todo remove it just for test
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
        table.setRowCount(len(adapters))
        table.setVerticalHeaderLabels(row_names)

        table.setColumnCount(1)
        table.setHorizontalHeaderLabels([" "])

        # load spectral params and locations
        for i in xrange(table.rowCount()):
            item = QtGui.QTableWidgetItem("")
            item.setCheckState(Qt.Unchecked)
            table.setItem(i, 0, item)

        table.cellClicked.connect(lambda x, y: self.select_parameter(adapters[x][1]))

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

        table.setRowCount(len(param_adapters))
        table.setColumnCount(len(locations_adapters))

        row_names = [x[0] for x in param_adapters]
        column_names = [x[0] for x in locations_adapters]

        # load spectral params and locations
        for i in xrange(table.rowCount()):
            for j in xrange(table.columnCount()):
                item = QtGui.QTableWidgetItem("")
                item.setCheckState(Qt.Unchecked)
                table.setItem(i, j, item)

        table.setVerticalHeaderLabels(row_names)
        table.setHorizontalHeaderLabels(column_names)

        table.cellClicked.connect(lambda x, y: self.select_parameter(param_adapters[x][1], locations_adapters[y][1]))

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    # endregion

    def create_settings_tree(self):
        # set the segmentation and classification parameters
        self.param_measurement_tree = Parameter.create(name=unicode(self.tr(u'Parameter Settings')), type=u'group')
        self.location_measurement_tree = Parameter.create(name=unicode(self.tr(u'Location Settings')), type=u'group')

        self.parameter_tree_widget.setParameters(self.param_measurement_tree)
        self.location_tree_widget.setParameters(self.location_measurement_tree)

    def select_parameter(self, parameter_adapter, location_adapter=None):
        """
        Execute the action of select a parameter on the window interface.
        Updates the param tree with the settings of selected parameter
        :param parameter_adapter: The parameter selected
        :param location_adapter: The (optional) location if any location
        selected for the parameter supplied
        :return:
        """
        self.param_measurement_tree.clearChildren()
        self.location_measurement_tree.clearChildren()

        if parameter_adapter is not None:
            param_settings = parameter_adapter.get_settings()

            if param_settings is not None:
                self.param_measurement_tree.addChild(param_settings)

        if location_adapter is not None:
            location_settings = location_adapter.get_settings()

            if location_settings is not None:
                self.location_measurement_tree.addChild(location_settings)

    def get_parameter_list(self):
        """
        :return: The list of parameters to measure
        """
        time_based_parameters = []

        table = self.time_parameter_table
        for i in xrange(table.rowCount()):
            if table.item(i, 0).checkState() == Qt.Checked:
                parameter = self.parameter_manager.time_parameters_adapters[i][1].get_instance()
                time_based_parameters.append(parameter)

        table = self.wave_parameter_table
        for i in xrange(table.rowCount()):
            if table.item(i, 0).checkState() == Qt.Checked:
                parameter = self.parameter_manager.wave_parameters_adapters[i][1].get_instance()
                time_based_parameters.append(parameter)

        spectral_parameters = []
        table = self.parameter_locations_table
        for i in xrange(table.rowCount()):
            for j in xrange(table.columnCount()):
                if table.item(i, j).checkState() == Qt.Checked:
                    parameter = self.parameter_manager.spectral_parameters_adapters[i][1].get_instance()
                    parameter.location = self.parameter_manager.locations_adapters[j][1].get_instance()
                    spectral_parameters.append(parameter)

        return time_based_parameters + spectral_parameters

    def closeEvent(self, *args, **kwargs):
        self.parameter_manager.parameter_list = self.get_parameter_list()

        self.parameters = self.parameter_manager.parameter_list

        QtGui.QDialog.closeEvent(self, *args, **kwargs)