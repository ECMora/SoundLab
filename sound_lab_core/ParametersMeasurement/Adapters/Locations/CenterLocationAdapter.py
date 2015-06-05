# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.FixedTimeLocationAdapter import FixedTimeLocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.CenterMeasurementLocation import CenterMeasurementLocation


class CenterLocationAdapter(FixedTimeLocationAdapter):

    def __init__(self):
        FixedTimeLocationAdapter.__init__(self)

        settings = [{u'name': unicode(self.tr(u'ms delay')), u'type': u'int',
                      u'value': 0, u'step': 1, u'limits': (- 60 * 60 * 1000, 60 * 60 * 1000)}]

        self.settings = Parameter.create(name=u'Time Location', type=u'group', children=settings)
        self.name = self.tr(u'Center')

    def get_instance(self):
        self.update_instance_variables()

        return [CenterMeasurementLocation(ms_delay=self.ms_delay)]




