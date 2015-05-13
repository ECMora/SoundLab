# -*- coding: utf-8 -*-


class MeasurementLocation:
    """
    Class that represent a measurement location of a parameter over a detected
    segment. A measurement location transform the way of compute the parameter.
    A parameter with a location is measured in a transformed segment data that
    just include the information of the segment location specified.
    """

    def __init__(self):
        # name of the measurement location
        self.name = ""

    def get_segment_data(self):
        """
        Compute and returns the segment data transformed accord to the current location
        to perform parameter measurement.
        to perform parameter measurement.
        :return:
        """
        return []


