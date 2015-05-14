from numpy import zeros
from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation
from matplotlib import mlab


class EndMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at the end of the segment.
    """

    def __init__(self, ms_delay=0):
        MeasurementLocation.__init__(self)

        self.ms_delay = 0 if ms_delay >= 0 else ms_delay

        self.name = "end" + "" if self.ms_delay == 0 else " - " + str(self.ms_delay) + "ms"

    def get_data_array_slice(self, segment):
        slice_arr = zeros(segment.indexTo - segment.indexFrom)
        slice_arr[: len(slice_arr) / 4] = segment.signal.data[segment.indexTo - len(slice_arr) / 4: segment.indexTo]
        return slice_arr