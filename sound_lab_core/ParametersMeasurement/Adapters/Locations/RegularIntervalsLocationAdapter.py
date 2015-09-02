# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.FixedTimeLocationAdapter import TimeLocationAdapter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.LocationAdapter import LocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.RegularIntervalsMeasurementLocation import \
    RegularIntervalsMeasurementLocation


class RegularIntervalsLocationAdapter(TimeLocationAdapter):
    """
    An adapter to create Regular Intervals Location.
    Those are the locations that divide the segment on n intervals
    and each interval are located on an equidistant distribution.
    """

    def __init__(self):
        TimeLocationAdapter.__init__(self)

        self.name = self.tr(u'Regular Intervals')

        self._settings.append({u'name': unicode(self.tr(u'Intervals')), u'type': u'int',
                               u'value': 4, u'step': 1, u'limits': (1, 10000)})

        # the amount of intervals to divide the segment
        self.intervals = 4

        self.settings = Parameter.create(name=u'Time Location', type=u'group', children=self._settings)

    def update_instance_variables(self):
        TimeLocationAdapter.update_instance_variables(self)
        try:
            intervals = self.settings.param(unicode(self.tr(u'Intervals'))).value()

        except Exception as e:
            intervals = 4

        self.intervals = intervals

    def get_instance(self):
        self.update_instance_variables()

        # create as many locations as the count of intervals selected
        return [RegularIntervalsMeasurementLocation(self.intervals, i, NFFT=self.fft_points, overlap=self.overlap)
                for i in xrange(self.intervals)]