from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import FrequencyMeasurementLocation


class MeanFrequencyMeasurementLocation(FrequencyMeasurementLocation):
    """
    Location of measurement at all the segment.
    """

    def __init__(self):
        FrequencyMeasurementLocation.__init__(self)
        self.name = "Mean"

    def get_data_array_slice(self, segment):
        return segment.signal.data[segment.indexFrom:segment.indexTo]