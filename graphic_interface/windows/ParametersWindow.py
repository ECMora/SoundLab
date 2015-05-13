#  -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from sound_lab_core.ParametersMeasurement.ParameterManager import ParameterManager
from ui_python_files.ParametersWindow import Ui_MainWindow


class ParametersWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    Window that visualize a parameter manager to change its configurations.
    """

    def __init__(self, parent=None, parameter_manager=None):
        """
        """
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # the manager to load the parameter configuration
        self.parameter_manager = parameter_manager if parameter_manager is not None else ParameterManager()
        self.load_parameter_config()

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

        self.parameter_locations_table.setVerticalHeaderLabels([x for x in self.parameter_manager.locations_adapters])
        self.parameter_locations_table.setHorizontalHeaderLabels([x for x in self.parameter_manager.spectral_parameters_adapters])

        self.parameter_locations_table.resizeColumnsToContents()
