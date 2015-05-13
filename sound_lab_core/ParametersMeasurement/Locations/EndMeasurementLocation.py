from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation


class EndMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at the end of the segment.
    """

    def __init__(self, ms_delay=0):
        MeasurementLocation.__init__(self)

        self.ms_delay = 0 if ms_delay >= 0 else ms_delay

        self.name = "end" + "" if self.ms_delay == 0 else " -" + self.ms_delay + " ms"