import numpy as np
from PyQt4.QtCore import QObject
from sound_lab_core.ParametersMeasurement.Adapters import *
from sound_lab_core.ParametersMeasurement.Adapters.Locations import *


class ParameterManager(QObject):
    """
    Class that handles the parameter measurement configurations.
    Provides the adapters for parameters creation.
    """

    def __init__(self):
        QObject.__init__(self)

        # adapters for each type of parameter
        self.time_parameters_adapters = [StartTimeParameterAdapter(), EndTimeParameterAdapter(),
                                         DurationTimeParameterAdapter(), ZeroCrossRateParameterAdapter(),
                                         LocalMaxMeanParameterAdapter(), EntropyTimeParameterAdapter()]

        self.wave_parameters_adapters = [RmsTimeParameterAdapter(), PeakToPeakParameterAdapter(),
                                         StartToMaxTimeParameterAdapter()]

        self.spectral_parameters_adapters = [PeakFreqParameterAdapter(), MaxFreqParameterAdapter(),
                                             MinFreqParameterAdapter(),  BandWidthParameterAdapter(),
                                             PeaksAboveParameterAdapter()]

        # location adapters of measurement for the spectral parameters
        self.locations_adapters = [StartLocationAdapter(), CenterLocationAdapter(),
                                   EndLocationAdapter(), MeanLocationAdapter()]

        rows, cols = len(self.spectral_parameters_adapters), len(self.locations_adapters)

        # matrix initialized on False
        self.location_parameters = np.zeros(rows * cols).reshape(rows, cols) > 0

    @property
    def parameter_list(self):
        """
        :return: The number of parameters
        """
        time_params = [x.get_instance() for x in self.time_parameters_adapters if x.selected]
        wave_params = [x.get_instance() for x in self.wave_parameters_adapters if x.selected]

        spectral_parameters = []
        for i in xrange(len(self.spectral_parameters_adapters)):
            for j in xrange(len(self.locations_adapters)):
                if self.location_parameters[i, j]:
                    parameter = self.spectral_parameters_adapters[i].get_instance()
                    parameter.location = self.locations_adapters[j].get_instance()
                    spectral_parameters.append(parameter)

        return time_params + wave_params + spectral_parameters
