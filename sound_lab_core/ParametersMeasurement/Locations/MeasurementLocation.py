# -*- coding: utf-8 -*-
from matplotlib import mlab


class MeasurementLocation:
    """
    Class that represent a measurement location of a parameter over a detected
    segment. A measurement location transform the way of compute the parameter.
    A parameter with a location is measured in a transformed segment data that
    just include the information of the segment location specified.

    A location is an interval (time and spectral) of the segment data
    """

    def __init__(self):
        # name of the measurement location
        self.name = ""

    def get_data_array_slice(self, segment):
        return segment.signal.data

    def get_segment_data(self, segment):
        """
        Compute and returns the segment data transformed accord to the current location
        to perform parameter measurement.
        to perform parameter measurement.
        :return:
        """
        return mlab.psd(self.get_data_array_slice(segment), Fs=segment.signal.samplingRate, noverlap=128)


class FrequencyMeasurementLocation(MeasurementLocation):

    def __init__(self):
        # name of the measurement location
        MeasurementLocation.__init__(self)
