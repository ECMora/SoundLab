import numpy as np
from PyQt4.QtCore import QObject
from sound_lab_core.ParametersMeasurement.Adapters import *
from sound_lab_core.ParametersMeasurement.Adapters.Locations import *


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

        # region Parameter adapters

        # adapters for each type of parameter
        self.time_parameters_adapters = [StartTimeParameterAdapter(), EndTimeParameterAdapter(),
                                         DurationTimeParameterAdapter()]

        self.wave_parameters_adapters = [RmsTimeParameterAdapter(), PeakToPeakParameterAdapter(),
                                         StartToMaxTimeParameterAdapter(), ZeroCrossRateParameterAdapter(),
                                         LocalMaxMeanParameterAdapter(), EntropyTimeParameterAdapter(),
                                         ShortTimeEnergyParameterAdapter()]

        self.spectral_parameters_adapters = [PeakFreqParameterAdapter(), MaxFreqParameterAdapter(),
                                             MinFreqParameterAdapter(),  BandWidthParameterAdapter(),
                                             PeaksAboveParameterAdapter(), DeltaSpectrumParameterAdapter(),
                                             SpectralCentroidParameterAdapter(), SpectralRollOffParameterAdapter(),
                                             SpectrumSpreadParameterAdapter(), WaveletMeanParameterAdapter(),
                                             WaveletCentroidParameterAdapter(), WaveletVarParameterAdapter(),
                                             WaveletDeltaParameterAdapter()
                                             ]

        # endregion

        # region Locations Adapters

        # time location adapters of measurement for the spectral parameters
        self.spectral_time_locations_adapters = [StartLocationAdapter(), CenterLocationAdapter(),
                                                 EndLocationAdapter(), MeanLocationAdapter(),
                                                 RegularIntervalsLocationAdapter(),
                                                 RegularDurationLocationAdapter()]
        
        # the time location adapters for the wave  parameters
        self.wave_locations_adapters = [StartLocationAdapter(), CenterLocationAdapter(),
                                        EndLocationAdapter(), MeanLocationAdapter(),
                                        RegularIntervalsLocationAdapter(),
                                        RegularDurationLocationAdapter()]

        # matrices for the selection of parameter-location (bool)
        rows, cols = len(self.wave_parameters_adapters), len(self.wave_locations_adapters)
        self.wave_location_parameters = np.zeros(rows * cols).reshape(rows, cols) > 0

        rows, cols = len(self.spectral_parameters_adapters), len(self.spectral_time_locations_adapters)
        self.spectral_location_parameters = np.zeros(rows * cols).reshape(rows, cols) > 0

        self.spectral_locations_adapters = np.array([FrequencyMeasurementLocationAdapter()
                                                     for _ in xrange(rows * cols)]).reshape((rows, cols))

        # endregion

        self.signal = signal
        if signal is not None:

            adapters = self.spectral_parameters_adapters + self.time_parameters_adapters + self.wave_parameters_adapters

            for adapter in adapters:
                adapter.update_data(signal)

            for i in xrange(self.spectral_locations_adapters.shape[0]):
                for j in xrange(self.spectral_locations_adapters.shape[1]):
                    self.spectral_locations_adapters[i, j].update_data(signal)
                    self.spectral_locations_adapters[i, j].allLocationsSharedChanged.\
                        connect(self.update_spectral_locations_shared_options)

    def update_spectral_locations_shared_options(self, spectral_adapter, share_location):
        """
        Updates the sharing options of the spectral locations.
        Switch between single location for all parameters or custom location for each one
        :return:
        """
        for i in xrange(self.spectral_locations_adapters.shape[0]):
            for j in xrange(self.spectral_locations_adapters.shape[1]):
                if share_location:
                    self.spectral_locations_adapters[i, j].restore_settings(spectral_adapter, self.signal)
                else:
                    self.spectral_locations_adapters[i, j].shared_locations = False

    def parameter_list(self):
        """
        :return: The number of parameters
        """
        time_params = [x.get_instance() for x in self.time_parameters_adapters]
        wave_params = []

        for i in xrange(len(self.wave_parameters_adapters)):
            for j in xrange(len(self.wave_locations_adapters)):
                if self.wave_location_parameters[i, j]:
                    for location in self.wave_locations_adapters[j].get_instance():
                        parameter = self.wave_parameters_adapters[i].get_instance()
                        parameter.time_location = location
                        wave_params.append(parameter)

        spectral_parameters = []
        for i in xrange(len(self.spectral_parameters_adapters)):
            for j in xrange(len(self.spectral_time_locations_adapters)):
                if self.spectral_location_parameters[i, j]:
                    for location in self.spectral_time_locations_adapters[j].get_instance():
                        spectral_location_adapter = self.spectral_locations_adapters[i, j]

                        for spectral_location in spectral_location_adapter.get_instance():
                            parameter = self.spectral_parameters_adapters[i].get_instance()
                            parameter.time_location = location
                            parameter.spectral_location = spectral_location
                            spectral_parameters.append(parameter)


        return time_params + wave_params + spectral_parameters
