# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.Locations.FixedTimeLocationAdapter import FixedTimeLocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.StartMeasurementLocation import StartMeasurementLocation


class StartLocationAdapter(FixedTimeLocationAdapter):

    def __init__(self):
        FixedTimeLocationAdapter.__init__(self)
        self.name = self.tr(u'Start')

    def get_instance(self):
        self.update_instance_variables()

        return [StartMeasurementLocation(ms_delay=self.ms_delay)]



