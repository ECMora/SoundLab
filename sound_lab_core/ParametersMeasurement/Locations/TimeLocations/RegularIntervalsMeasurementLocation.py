from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation


class RegularIntervalsMeasurementLocation(MeasurementLocation):
    """
    Locations that represents an x-distant division of a segment in n sub-intervals
    """

    def __init__(self, interval_count, subinterval_index, NFFT, overlap):
        """
        :param interval_count: The amount of intervals that is divided the
        segment for the current location.
        :param subinterval_index: the index of the current sub-interval location
        :return:
        """
        MeasurementLocation.__init__(self, NFFT, overlap)

        self.name = "Regular Intervals" + "[" + str(subinterval_index + 1) + "]"

        self.interval_count = interval_count
        self.sub_interval_index = subinterval_index

    def get_data_array_slice(self, segment):
        interval_length = (segment.indexTo - segment.indexFrom) / self.interval_count

        start_index = min(segment.indexFrom + interval_length * self.sub_interval_index,
                          segment.indexTo - self.NFFT)

        end_index = start_index + self.NFFT

        self.time_start_index, self.time_end_index = start_index, end_index

        return segment.signal.data[start_index:end_index]