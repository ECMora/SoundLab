# -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject
from sound_lab_core.ParametersMeasurement.Locations.MeanMeasurementLocation import MeanMeasurementLocation


class ParameterMeasurer(QObject):
    """
    Class that represent an object that measure parameters
    in segments.
    """

    def __init__(self, decimal_places=2, measurement_location=None):
        """
        Create a parameter measurer
        :return:
        """
        QObject.__init__(self)

        # the name of the parameter
        self._name = ""

        # the decimal places to round this parameter
        self._decimal_places = decimal_places

        # the location on the detected segment to perform the parameter measurement
        self._measurement_location = measurement_location

        if self._measurement_location is None:
            self._measurement_location = MeanMeasurementLocation()

    def getName(self):
        return self.name

    # region Properties

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, (str, unicode)):
            raise Exception("Invalid type for name. Must be str or unicode.")

        self._name = new_name

    @property
    def decimal_places(self):
        return self._decimal_places

    @decimal_places.setter
    def decimal_places(self, new_decimal_places):
        if not isinstance(new_decimal_places, int):
            raise Exception("Invalid type for decimal_places. Must be int.")
        self._decimal_places = new_decimal_places

    @property
    def location(self):
        return self._measurement_location

    @location.setter
    def location(self, new_location):
        if new_location is None:
            raise Exception("Location of measurement cant be None")

        self._measurement_location = new_location

    # endregion

    def __str__(self):
        return self.name

    def get_visual_items(self):
        return []

    @property
    def default_value(self):
        """
        :return: The default Value for the current parameter
        """
        return 0

    def measure(self, segment):
        """
        Abstract method that performs the measure of the
        parameter over the supplied segment.
        :type data: numpy array with the signal
        :param segment:
        :return:
        """
        pass