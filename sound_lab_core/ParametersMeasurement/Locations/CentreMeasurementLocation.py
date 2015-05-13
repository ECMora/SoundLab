from sound_lab_core.ParametersMeasurement.Locations.MeasurementLocation import MeasurementLocation

__author__ = 'y.febles'


class CentreMeasurementLocation(MeasurementLocation):
    """
    Location of measurement at the centre of the segment.
    """

    def __init__(self, ms_delay=0):
        MeasurementLocation.__init__(self)

        self.ms_delay = ms_delay

        self.name = "centre"

        if self.ms_delay > 0:
            self.name += " +" + self.ms_delay + " ms"

        if self.ms_delay < 0:
            self.name += " -" + self.ms_delay + " ms"