# -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject, pyqtSignal

from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.MeanMeasurementLocation import MeanMeasurementLocation


class ParameterMeasurer(QObject):
    """
    Class that represent an object that measure parameters
    in segments.
    """

    # signal raised when the time location is changed
    timeLocationChanged = pyqtSignal()

    def __init__(self, decimal_places=2, time_measurement_location=None, visual_items=None):
        """
        Create a parameter measurer
        :return:
        """
        QObject.__init__(self)

        # the name of the parameter
        self._name = ""

        self.visual_items = [] if visual_items is None or not isinstance(visual_items, list) else visual_items

        # the decimal places to round this parameter
        self._decimal_places = decimal_places

        # the location on the detected segment to perform the parameter measurement
        self._time_measurement_location = time_measurement_location

    def getName(self):
        time_location_name = "(" + self.time_location.name + ")" if self.time_location is not None else ""

        return self._name + time_location_name

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
    def time_location(self):
        return self._time_measurement_location

    @time_location.setter
    def time_location(self, new_location):
        if new_location is None:
            raise Exception("Location of measurement cant be None")

        self._time_measurement_location = new_location
        self.timeLocationChanged.emit()

    # endregion

    def __eq__(self, other):
        return type(self) == type(other)

    def __str__(self):
        return self.name

    def get_visual_items(self):
        return self.visual_items

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