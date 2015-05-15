from PyQt4.QtCore import QObject, pyqtSignal
from sound_lab_core.ParametersMeasurement.Adapters import *
from sound_lab_core.ParametersMeasurement.Adapters.Locations import *


class ParameterManager(QObject):
    """
    Class that handles the parameter measurement configurations.
    Provides the adapters for parameters creation.
    """

    def __init__(self):
        QObject.__init__(self)

        # location adapters of measurement for the spectral parameters
        self.locations_adapters = [(u'Start', StartLocationAdapter()),
                                   (u'Center', CenterLocationAdapter()),
                                   (u'End', EndLocationAdapter()),
                                   (u'Mean', MeanLocationAdapter())]

        # adapters for each type of parameter
        self.time_parameters_adapters = [
            (u'Start Time', StartTimeParameterAdapter()),
            (u'End Time', EndTimeParameterAdapter()),
            (u'Duration', DurationTimeParameterAdapter()),
            (u'Zero Cross Rate', ZeroCrossRateParameterAdapter()),
            (u'Local Max Mean', LocalMaxMeanParameterAdapter()),
            (u'Entropy', EntropyTimeParameterAdapter())]

        self.wave_parameters_adapters = [
            (u'RMS', RmsTimeParameterAdapter()),
            (u'PeakToPeak', PeakToPeakParameterAdapter()),
            (u'StartToMax', StartToMaxTimeParameterAdapter())]

        self.spectral_parameters_adapters = [
            (u'PeakFreq', PeakFreqParameterAdapter()),
            (u'MaxFreq', MaxFreqParameterAdapter()),
            (u'MinFreq', MinFreqParameterAdapter()),
            (u'BandWidth', BandWidthParameterAdapter()),
            (u'PeaksAbove', PeaksAboveParameterAdapter())]

        self._parameter_list = []

    @property
    def count(self):
        """
        :return: The number of parameters
        """
        return len(self.parameter_list)

    @property
    def parameter_list(self):
        """
        :return: The number of parameters
        """
        return self._parameter_list

    @parameter_list.setter
    def parameter_list(self, new_param_list):
        self._parameter_list = new_param_list