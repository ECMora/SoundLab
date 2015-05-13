# -*- coding: utf-8 -*-


class ParameterMeasurer:
    """
    Class that represent an object that measure parameters
    in segments.
    """

    def __init__(self, decimal_places=2, measurement_location=None):
        """
        Create a parameter measurer
        :return:
        """

        # the name of the parameter
        self._name = ""

        # the decimal places to round this parameter
        self._decimal_places = decimal_places

        # the location on the detected segment to perform the parameter measurement
        self._measurement_location = measurement_location

    # region Properties

    @property
    def name(self):
        location_name = "" if self.location is None else self.location.name
        return self._name + "(" + location_name + ")"

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
        self._measurement_location = new_location

    # endregion

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