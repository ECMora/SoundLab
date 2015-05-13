from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation


class StartMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at the start of the segment.
    """

    def __init__(self, ms_delay=0):
        MeasurementLocation.__init__(self)

        self.ms_delay = 0 if ms_delay <= 0 else ms_delay

        self.name = "start" + "" if self.ms_delay == 0 else " +" + self.ms_delay + " ms"