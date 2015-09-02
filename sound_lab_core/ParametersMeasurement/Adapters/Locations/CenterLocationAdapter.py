# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.FixedTimeLocationAdapter import FixedTimeLocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.CenterMeasurementLocation import CenterMeasurementLocation


class CenterLocationAdapter(FixedTimeLocationAdapter):
    """
    The FixedTimeLocationAdapter for the centre of the segment
    """

    def __init__(self):
        FixedTimeLocationAdapter.__init__(self)

        self.settings.param(unicode(self.tr(u'ms delay'))).setLimits((-1000000, 1000000))

        self.name = self.tr(u'Center')

    def get_instance(self):
        self.update_instance_variables()

        return [CenterMeasurementLocation(ms_delay=self.ms_delay, NFFT=self.fft_points, overlap=self.overlap)]




