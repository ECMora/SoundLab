from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation


class RegularDurationMeasurementLocation(MeasurementLocation):
    """
    Locations that represents an x-distant division
    of a segment every duration_interval_ms of time.
    """

    def __init__(self, duration_interval_ms, subinterval_index, NFFT, overlap):
        """
        :param duration_interval_ms: The duration of the intervals in
        which is divided the segment for the current location.
        :param subinterval_index: the index of the current sub-interval location
        :return:
        """
        MeasurementLocation.__init__(self, NFFT, overlap)

        self.name = "Regular Duration" + "[" + str((subinterval_index + 1) * duration_interval_ms) + "ms]"

        self.interval_duration = duration_interval_ms
        self.sub_interval_index = subinterval_index

    def get_data_array_slice(self, segment):
        return segment.signal.data[segment.indexFrom:segment.indexTo]