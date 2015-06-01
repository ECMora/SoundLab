import numpy as np
from PyQt4.QtCore import QObject
from sound_lab_core.ParametersMeasurement.Adapters import *
from sound_lab_core.ParametersMeasurement.Adapters.Locations import *
from sound_lab_core.ParametersMeasurement.Adapters.Locations.RegularDurationLocationAdapter import \
    RegularDurationLocationAdapter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.RegularIntervalsLocationAdapter import \
    RegularIntervalsLocationAdapter


class ParameterManager(QObject):
    """
    Class that handles the parameter measurement configurations.
    Provides the adapters for parameters creation.
    """

    def __init__(self, signal=None):
        """
        :param signal: the signal in which would be be measured the parameters.
        :return:
        """
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

        # time location adapters of measurement for the spectral parameters
        self.time_locations_adapters = [StartLocationAdapter(), CenterLocationAdapter(),
                                        EndLocationAdapter(), MeanLocationAdapter(),
                                        RegularIntervalsLocationAdapter(),
                                        RegularDurationLocationAdapter()]

        rows, cols = len(self.spectral_parameters_adapters), len(self.time_locations_adapters)

        # matrix of selection for initialized on False
        self.location_parameters = np.zeros(rows * cols).reshape(rows, cols) > 0

        if signal is not None:
            adapters = self.spectral_parameters_adapters + self.time_parameters_adapters + self.wave_parameters_adapters

            for adapter in adapters:
                adapter.update_data(signal)

        self.spectral_locations = []

    def parameter_list(self):
        """
        :return: The number of parameters
        """
        time_params = [x.get_instance() for x in self.time_parameters_adapters if x.selected]
        wave_params = [x.get_instance() for x in self.wave_parameters_adapters if x.selected]

        spectral_parameters = []
        for i in xrange(len(self.spectral_parameters_adapters)):
            for j in xrange(len(self.time_locations_adapters)):
                if self.location_parameters[i, j]:
                    for location in self.time_locations_adapters[j].get_instance():
                        spectral_location_adapter = self.spectral_parameters_adapters[i].get_spectral_location_adapter()

                        for spectral_location in spectral_location_adapter.get_instance():
                            parameter = self.spectral_parameters_adapters[i].get_instance()
                            parameter.time_location = location
                            parameter.spectral_location = spectral_location
                            spectral_parameters.append(parameter)

        return time_params + wave_params + spectral_parameters
