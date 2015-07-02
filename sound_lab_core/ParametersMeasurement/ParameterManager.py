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
        self.spectral_time_locations_adapters = [MeanLocationAdapter(), StartLocationAdapter(),
                                                 CenterLocationAdapter(), EndLocationAdapter(),
                                                 RegularIntervalsLocationAdapter(),
                                                 RegularDurationLocationAdapter()]
        
        # the time location adapters for the wave  parameters (same locations that the )
        self.wave_locations_adapters = [x.__class__() for x in self.spectral_time_locations_adapters]

        # endregion

        # matrices for the selection of parameter-location (bool)
        self.time_location_parameters = np.zeros(len(self.time_parameters_adapters)) > 0

        rows, cols = len(self.wave_parameters_adapters), len(self.wave_locations_adapters)
        self.wave_location_parameters = np.zeros(rows * cols).reshape(rows, cols) > 0

        rows, cols = len(self.spectral_parameters_adapters), len(self.spectral_time_locations_adapters)
        self.spectral_location_parameters = np.zeros(rows * cols).reshape(rows, cols) > 0

        self.spectral_locations_adapters = np.array([FrequencyMeasurementLocationAdapter()
                                                     for _ in xrange(rows * cols)]).reshape((rows, cols))

        self.signal = signal
        if signal is None:
            return

        adapters = self.spectral_parameters_adapters + self.time_parameters_adapters + self.wave_parameters_adapters
        
        # updates the adapters with the signal properties
        for adapter in adapters:
            adapter.update_data(signal)
        
        # update connections to react when a share freq location option has changed 
        for i in xrange(self.spectral_locations_adapters.shape[0]):
            for j in xrange(self.spectral_locations_adapters.shape[1]):
                
                self.spectral_locations_adapters[i, j].update_data(signal)
                self.spectral_locations_adapters[i, j].allLocationsSharedChanged.connect(self.spectral_locations_share_changed)

    def spectral_locations_share_changed(self, spectral_adapter, share_location):
        """
        Updates the sharing options of the spectral locations.
        Switch between single location for all parameters or custom location for each one
        :type share_location: True if share the location for all the parameters False otherwise
        :type spectral_adapter: the spectral adapter to update
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
        :return: The list with all the parameters to measure.
        """
        time_params = [x.get_instance() for x in self.time_parameters_adapters]

        # compute the wave parameter accords to the param-location selected
        wave_params = []
        for i in xrange(len(self.wave_parameters_adapters)):
            for j in xrange(len(self.wave_locations_adapters)):
                if self.wave_location_parameters[i, j]:

                    # add as many parameters-locations as locations selected
                    for location in self.wave_locations_adapters[j].get_instance():

                        parameter = self.wave_parameters_adapters[i].get_instance()
                        parameter.time_location = location
                        wave_params.append(parameter)

        # compute the wave parameter accords to the param-location selected
        spectral_parameters = []
        for i in xrange(len(self.spectral_parameters_adapters)):
            for j in xrange(len(self.spectral_time_locations_adapters)):
                if self.spectral_location_parameters[i, j]:

                    # add as many parameters-locations as locations selected. In this case
                    # there is two types of locations: time and spectral
                    for location in self.spectral_time_locations_adapters[j].get_instance():
                        spectral_location_adapter = self.spectral_locations_adapters[i, j]

                        for spectral_location in spectral_location_adapter.get_instance():

                            parameter = self.spectral_parameters_adapters[i].get_instance()
                            parameter.time_location = location
                            parameter.spectral_location = spectral_location
                            spectral_parameters.append(parameter)

        return time_params + wave_params + spectral_parameters

    def clone(self):
        return self