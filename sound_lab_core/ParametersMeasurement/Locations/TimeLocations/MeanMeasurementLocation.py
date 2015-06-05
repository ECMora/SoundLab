from matplotlib import mlab
from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation


class MeanMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at all the segment.
    """

    def __init__(self):
        MeasurementLocation.__init__(self)
        self.name = "Mean"

    def get_data_array_slice(self, segment):
        return segment.signal.data[segment.indexFrom:segment.indexTo]