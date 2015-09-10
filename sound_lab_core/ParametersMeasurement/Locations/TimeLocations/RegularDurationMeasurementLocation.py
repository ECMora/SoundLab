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

        self.name = u"Regular Duration" + u"[" + unicode((subinterval_index + 1) * duration_interval_ms) \
                    + u"ms]"

        self.interval_duration = duration_interval_ms
        self.sub_interval_index = subinterval_index

    def get_data_array_slice(self, segment):
        sr = segment.signal.samplingRate
        interval_length = sr * self.interval_duration / 1000.0

        start_index = segment.indexFrom + interval_length * self.sub_interval_index

        if start_index >= segment.indexTo:
            raise Exception("The location requested is outside the segment")

        end_index = min(start_index + self.NFFT, segment.indexTo)

        self.time_start_index, self.time_end_index = start_index, end_index

        return segment.signal.data[start_index:end_index]