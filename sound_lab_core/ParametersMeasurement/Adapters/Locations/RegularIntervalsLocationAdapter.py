# -*- coding: utf-8 -*-
from sound_lab_core.ParametersMeasurement.Adapters.Locations.FixedTimeLocationAdapter import LocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.RegularIntervalsMeasurementLocation import \
    RegularIntervalsMeasurementLocation
from pyqtgraph.parametertree import Parameter


class RegularIntervalsLocationAdapter(LocationAdapter):
    def __init__(self):
        LocationAdapter.__init__(self)
        self.name = self.tr(u'Regular Intervals')

        settings = [{u'name': unicode(self.tr(u'Intervals')), u'type': u'int',
                     u'value': 4, u'step': 1, u'limits': (1, 10000)}]

        self.intervals = 4

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def update_instance_variables(self):
        try:
            intervals = self.settings.param(unicode(self.tr(u'Intervals'))).value()

        except Exception as e:
            intervals = 4

        self.intervals = intervals

    def get_instance(self):
        self.update_instance_variables()

        locations = []

        for i in xrange(self.intervals):
            locations.append(RegularIntervalsMeasurementLocation(self.intervals, i))

        return locations

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings




