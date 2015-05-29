from sound_lab_core.ParametersMeasurement.Locations.FrequencyMeasurementLocation import FrequencyMeasurementLocation


class RegularDurationFrequencyMeasurementLocation(FrequencyMeasurementLocation):
    """
    Locations that represents an x-distant division
    of a segment every duration_interval_ms of time.
    """

    def __init__(self, duration_interval_ms, subinterval_index, min_kHz=0, max_kHz=250):
        """
        :param duration_interval_ms: The duration of the intervals in
        which is divided the segment for the current location.
        :param subinterval_index: the index of the current sub-interval location
        :return:
        """
        FrequencyMeasurementLocation.__init__(self, min_kHz=min_kHz, max_kHz=max_kHz)

        self.name = "Regular Duration" + "[" + str((subinterval_index + 1) * duration_interval_ms) + "ms]"

        self.interval_duration = duration_interval_ms
        self.sub_interval_index = subinterval_index

    def get_data_array_slice(self, segment):
        return segment.signal.data[segment.indexFrom:segment.indexTo]