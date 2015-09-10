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

        self.name = u"Regular Intervals" + u"[" + unicode(subinterval_index + 1) + u"]"

        self.interval_count = interval_count
        self.sub_interval_index = subinterval_index

    def get_data_array_slice(self, segment):
        interval_length = (segment.indexTo - segment.indexFrom) / self.interval_count

        start_index = segment.indexFrom + interval_length * self.sub_interval_index

        if start_index >= segment.indexTo:
            raise Exception("The location requested is outside the segment")

        end_index = min(start_index + self.NFFT, segment.indexTo)

        self.time_start_index, self.time_end_index = start_index, end_index

        return segment.signal.data[start_index:end_index]