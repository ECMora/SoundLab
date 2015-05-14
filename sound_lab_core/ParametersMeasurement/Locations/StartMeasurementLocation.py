from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation
from numpy import zeros


class StartMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at the start of the segment.
    """

    def __init__(self, ms_delay=0):
        MeasurementLocation.__init__(self)

        self.ms_delay = 0 if ms_delay <= 0 else ms_delay

        self.name = "start" + "" if self.ms_delay == 0 else " + " + str(self.ms_delay) + "ms"

    def get_data_array_slice(self, segment):
        slice_arr = zeros(segment.indexTo - segment.indexFrom)
        slice_arr[: len(slice_arr) / 4] = segment.signal.data[segment.indexFrom: segment.indexFrom + len(slice_arr) / 4]
        return slice_arr