from sound_lab_core.ParametersMeasurement.Locations.FrequencyMeasurementLocation import FrequencyMeasurementLocation


class MeanFrequencyMeasurementLocation(FrequencyMeasurementLocation):
    """
    Location of measurement at all the segment.
    """

    def __init__(self, min_kHz=0, max_kHz=250):
        FrequencyMeasurementLocation.__init__(self, min_kHz=min_kHz, max_kHz=max_kHz)
        self.name = "Mean"

    def get_data_array_slice(self, segment):
        return segment.signal.data[segment.indexFrom:segment.indexTo]