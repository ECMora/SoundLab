from sound_lab_core.ParametersMeasurement.Locations.FrequencyMeasurementLocation import FrequencyMeasurementLocation


class RegularIntervalsFrequencyMeasurementLocation(FrequencyMeasurementLocation):
    """
    Locations that represents an x-distant division of a segment in n sub-intervals
    """

    def __init__(self, interval_count, subinterval_index, min_kHz=0, max_kHz=250):
        """
        :param interval_count: The amount of intervals that is divided the
        segment for the current location.
        :param subinterval_index: the index of the current sub-interval location
        :return:
        """
        FrequencyMeasurementLocation.__init__(self, min_kHz=min_kHz, max_kHz=max_kHz)

        self.name = "Regular Intervals" + "[" + str(subinterval_index + 1) + "]"

        self.interval_count = interval_count
        self.sub_interval_index = subinterval_index

    def get_data_array_slice(self, segment):
        return segment.signal.data[segment.indexFrom:segment.indexTo]