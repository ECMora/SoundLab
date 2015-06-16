# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter

from sound_lab_core.ParametersMeasurement.Adapters.Locations.LocationAdapter import LocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.RegularDurationMeasurementLocation import \
    RegularDurationMeasurementLocation


class RegularDurationLocationAdapter(LocationAdapter):
    """
    A time location adapter to define a group of locations in a segment.
    The RegularDurationLocationAdapter allows to define n equidistant
    locations on a segment each one separated by a  time delay in ms.
    """
    def __init__(self):
        LocationAdapter.__init__(self)
        self.name = self.tr(u'Regular Duration')

        settings = [{u'name': unicode(self.tr(u'duration (ms)')), u'type': u'int',
                     u'value': 100, u'step': 1, u'limits': (1, 100000)},
                    {u'name': unicode(self.tr(u'max intervals')), u'type': u'int',
                     u'value': 20, u'step': 1, u'limits': (1, 100000)}]

        self.duration_ms = 100
        self.max_intervals = 20

        self.settings = Parameter.create(name=u'Time Location', type=u'group', children=settings)

    def get_instance(self):
        try:
            duration_ms = self.settings.param(unicode(self.tr(u'duration (ms)'))).value()
            max_intervals = self.settings.param(unicode(self.tr(u'max intervals'))).value()

        except Exception as e:
            duration_ms = 100
            max_intervals = 100

        self.duration_ms = duration_ms
        self.max_intervals = max_intervals
        locations = []

        for i in xrange(self.max_intervals):
            locations.append(RegularDurationMeasurementLocation(self.duration_ms, i))

        return locations

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings




