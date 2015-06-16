# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter

from sound_lab_core.ParametersMeasurement.Adapters.Locations.LocationAdapter import LocationAdapter


class FixedTimeLocationAdapter(LocationAdapter):
    """
    Location adapter for the locations of time, those are the locations that
    define a time piece of the segment to perform the parameter measurements.
    """

    def __init__(self):
        LocationAdapter.__init__(self)

        settings = [{u'name': unicode(self.tr(u'ms delay')), u'type': u'int',
                     u'value': 0, u'step': 1, u'limits': (0, 60 * 60 * 1000)}]

        # the time delay in ms of the time location
        self.ms_delay = 0

        self.settings = Parameter.create(name=u'Time Location', type=u'group', children=settings)

    def update_instance_variables(self):
        try:
            ms_delay = self.settings.param(unicode(self.tr(u'ms delay'))).value()

        except Exception as e:
            ms_delay = 0

        self.ms_delay = ms_delay