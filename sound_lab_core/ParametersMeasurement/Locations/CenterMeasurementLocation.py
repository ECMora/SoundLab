from numpy import zeros
from matplotlib import mlab
from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation


class CenterMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at the centre of the segment.
    """

    def __init__(self, ms_delay=0):
        MeasurementLocation.__init__(self)

        self.ms_delay = ms_delay

        self.name = "center"

        if self.ms_delay > 0:
            self.name += " + " + str(self.ms_delay) + "ms"

        if self.ms_delay < 0:
            self.name += " - " + str(self.ms_delay) + "ms"

    def get_data_array_slice(self, segment):
        slice_arr = zeros(segment.indexTo - segment.indexFrom)

        centre = segment.indexFrom + (segment.indexTo - segment.indexFrom) / 2

        slice_arr[: len(slice_arr) / 4] = segment.signal.data[centre - len(slice_arr) / 8: centre + len(slice_arr) / 8]
        return slice_arr