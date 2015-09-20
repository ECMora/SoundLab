# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Locations.SpectralLocations.FrequencyMeasurementLocation import \
    FrequencyMeasurementLocation
from sound_lab_core.ParametersMeasurement.ParameterMeasurer import ParameterMeasurer
from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.MeanMeasurementLocation import MeanMeasurementLocation


class SpectralParameter(ParameterMeasurer):
    """
    Class that measure the min freq parameter on a segment
    """

    def __init__(self, spectral_measurement_location=None, **kwargs):
        ParameterMeasurer.__init__(self, **kwargs)

        # the location on the detected segment to perform the spectral parameter measurement
        self._spectral_measurement_location = spectral_measurement_location

        if self._spectral_measurement_location is None:
            self._spectral_measurement_location = FrequencyMeasurementLocation()

        self.timeLocationChanged.connect(self._update_visual_items)

    @property
    def spectral_location(self):
        return self._spectral_measurement_location

    @spectral_location.setter
    def spectral_location(self, new_location):
        if new_location is None:
            raise Exception("Location of measurement cant be None")

        self._spectral_measurement_location = new_location

    def _update_visual_items(self):
        """
        The visual item for the peak freq parameter changes with the location.
        if location is 'mean' must be connected the start and end of the location
        if not just visualize the start point.
        :return:
        """
        connect_points = isinstance(self.time_location, MeanMeasurementLocation)

        for item in self.visual_items:
            item.connect_points = connect_points
    def getName(self):
        """
        :return: The name and the location (if any)
        """
        time_location_name = "" if self.time_location is None else self.time_location.name
        # spectral_location_name = "" if self.spectral_location is None else self.spectral_location.name

        return self._name + "(" + time_location_name + ")"  #(" + spectral_location_name + ")"


class FreqParameter(SpectralParameter):
    """
    Class that measure the min freq parameter on a segment
    """

    def __init__(self, threshold=-20, total=True, **kwargs):
        SpectralParameter.__init__(self, **kwargs)

        self.threshold = threshold
        self.total = total
