import numpy as np
from sound_lab_core.ParametersMeasurement.Adapters import *
from sound_lab_core.ParametersMeasurement.Adapters.Locations import *


class MeasurementTemplate:
    """
    Class that handles the parameter measurement configurations.
    Defines a template for measurements that  holds information
    about a parameter measurement configuration made by user or
    provided  by  sound lab  system. Allow  to  create  specific
    parameter  selection to process  specific  group of signals.
    """

    def __init__(self, signal=None, editable=True, name=""):
        """
        :param signal: the signal in which would be be measured the parameters.
        :param editable: True if the configuration allow edition. False otherwise
        :param name: the name of the measurement template
        :return:
        """

        self.name = name
        self.editable = editable

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
                                             PeaksAboveParameterAdapter()]

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

        self.update_adapters_data(signal)

    def update_adapters_data(self, signal=None, spectrogram_data=None):

        if signal is not None:
            # if there is a signal provided then update the adapters values for it
            adapters = self.spectral_parameters_adapters + self.time_parameters_adapters + self.wave_parameters_adapters

            # updates the adapters with the signal properties
            for adapter in adapters:
                adapter.update_data(signal)

        if spectrogram_data is not None:
            pass

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

                    # add as many parameters-locations as locations selected.
                    for location in self.spectral_time_locations_adapters[j].get_instance():
                        parameter = self.spectral_parameters_adapters[i].get_instance()
                        parameter.time_location = location
                        spectral_parameters.append(parameter)

        return time_params + wave_params + spectral_parameters

    def clone(self):
        return self

    def get_state(self):
        return dict(name=self.name, editable=self.editable,

                    # boolean matrix of selections
                    time_location=self.time_location_parameters,
                    wave_location=self.wave_location_parameters,
                    spectral_location=self.spectral_location_parameters,

                    # parameter adapters states
                    time_parameters_adapters=[x.state() for x in self.time_parameters_adapters],
                    wave_parameters_adapters=[x.state() for x in self.wave_parameters_adapters],
                    spectral_parameters_adapters=[x.state() for x in self.spectral_parameters_adapters],

                    # location adapters states
                    wave_locations_adapters=[x.state() for x in self.wave_locations_adapters],
                    spectral_time_locations_adapters=[x.state() for x in self.spectral_time_locations_adapters])

    def load_state(self, state):
        """
        load into the current instance a saved state of a measurement template
        :param state: dict with the state saved
        :return:
        """

        if not isinstance(state, dict):
            return

        self.name = state["name"] if "name" in state else self.name
        self.editable = state["editable"] if "editable" in state else self.editable

        # region matrix with boolean selections

        if "time_location" in state:
            self.time_location_parameters = state["time_location"]

        if "wave_location" in state:
            self.wave_location_parameters = state["wave_location"]

        if "spectral_location" in state:
            self.spectral_location_parameters = state["spectral_location"]

        # endregion

        # parameter adapters

        self.__load_state_helper(state, "time_parameters_adapters", self.time_parameters_adapters)
        self.__load_state_helper(state, "wave_parameters_adapters", self.wave_parameters_adapters)
        self.__load_state_helper(state, "spectral_parameters_adapters", self.spectral_parameters_adapters)

        # location adapters
        self.__load_state_helper(state, "wave_locations_adapters", self.wave_locations_adapters)
        self.__load_state_helper(state, "spectral_time_locations_adapters", self.spectral_time_locations_adapters)

    def __load_state_helper(self, state, field_name, field):

        if field_name in state:
            for i in xrange(len(field)):
                try:
                    field[i].load_state(state[field_name][i])

                except Exception as e:
                    print("Error in load state of measurement template. " + e.message)
