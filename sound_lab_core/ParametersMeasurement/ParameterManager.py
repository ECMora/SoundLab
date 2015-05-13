from PyQt4.QtCore import QObject, pyqtSignal
from Locations import *
from sound_lab_core.ParametersMeasurement.Adapters import *


class ParameterManager(QObject):
    """
    Class that handles the parameter measurement configurations.
    Its a
    """

    def __init__(self):
        QObject.__init__(self)

        # location adapters of measurement for the spectral parameters
        self.locations_adapters = [StartMeasurementLocation(),
                                   MeanMeasurementLocation(),
                                   EndMeasurementLocation(),
                                   CentreMeasurementLocation()]

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