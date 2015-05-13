#  -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from pyqtgraph.parametertree import Parameter, ParameterTree
from sound_lab_core.ParametersMeasurement.ParameterManager import ParameterManager
from ui_python_files.ParametersWindow import Ui_MainWindow


class ParametersWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    Window that visualize a parameter manager to change its configurations.
    """

    def __init__(self, parent=None, parameter_manager=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.save_bttn.clicked.connect(self.close)

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

        # the manager to load the parameter configuration
        self._parameter_manager = None
        self.parameter_manager = parameter_manager if parameter_manager is not None else ParameterManager()

    # region Properties

    @property
    def parameter_manager(self):
        return self._parameter_manager

    @parameter_manager.setter
    def parameter_manager(self, parameter):
        self._parameter_manager = parameter
        self.load_parameter_config()

    # endregion

    def load_parameter_config(self):
        """
        Load into the window the parameter configuration on its
        parameter_manager.
        :return:
        """
        if self.parameter_manager is None:
            return

        self.parameter_locations_table.setRowCount(len(self.parameter_manager.locations_adapters))
        self.parameter_locations_table.setColumnCount(len(self.parameter_manager.spectral_parameters_adapters))

        for i in xrange(self.parameter_locations_table.rowCount()):
            for j in xrange(self.parameter_locations_table.columnCount()):
                item = QtGui.QTableWidgetItem("")
                item.setCheckState(Qt.Unchecked)
                self.parameter_locations_table.setItem(i, j, item)

        row_names = [x.name for x in self.parameter_manager.locations_adapters]
        column_names = [x[0] for x in self.parameter_manager.spectral_parameters_adapters]

        self.parameter_locations_table.setVerticalHeaderLabels(row_names)
        self.parameter_locations_table.setHorizontalHeaderLabels(column_names)
        self.parameter_locations_table.cellClicked.connect(lambda x, y: self.select_parameter(
            self.parameter_manager.spectral_parameters_adapters[y],
            self.parameter_manager.locations_adapters[x]))

        self.parameter_locations_table.resizeColumnsToContents()
        self.parameter_locations_table.resizeRowsToContents()
        self.create_settings_tree()

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
            param_settings = parameter_adapter[1].get_settings()

            if param_settings is not None:
                self.param_measurement_tree.addChild(param_settings)

        # if location_adapter is not None:
        #     location_settings = location_adapter.get_settings()
        #
        #     if location_settings is not None:
        #         self.location_measurement_tree.addChild(param_settings)

