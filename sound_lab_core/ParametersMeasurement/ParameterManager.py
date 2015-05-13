from PyQt4.QtCore import QObject, pyqtSignal


class ParameterManager(QObject):
    """
    Class that handles the parameter measurement configurations.
    Its a
    """

    def __init__(self):
        QObject.__init__(self)

        # location of measurement for the spectral parameters
        self.locations_adapters = ["Start", "End", "Mean"]

        # adapters for each type of parameter
        self.time_parameters_adapters = []
        self.wave_parameters_adapters = []
        self.spectral_parameters_adapters = ["Peak freq", "Max freq", "Min freq"]

    @property
    def count(self):
        """
        :return: The number of parameters
        """
        return len(self.get_parameter_list())

    def get_parameter_list(self):
        """
        Computes and returns the list with all parameters instances for measurements
        :return:
        """
        return []