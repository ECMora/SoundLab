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

    def __init__(self, NFFT=512, overlap=50):
        # name of the measurement location
        self.name = ""

        self.NFFT = NFFT

        # overlap in %
        self.overlap = int(overlap * 0.01 * NFFT)

        self.time_start_index, self.time_end_index = 0, 0

    def get_data_array_slice(self, segment):
        """
        Returns the slice of segment data that belongs to the current location.
        :param segment:
        :return:
        """
        return segment.signal.data[segment.indexFrom:segment.indexTo]

    def get_segment_data(self, segment):
        """
        Compute and returns the segment data transformed accord to the current location
        to perform parameter measurement.
        :return:
        """
        data = self.get_data_array_slice(segment)
        return mlab.psd(data, NFFT=self.NFFT, Fs=segment.signal.samplingRate, noverlap=self.overlap)


