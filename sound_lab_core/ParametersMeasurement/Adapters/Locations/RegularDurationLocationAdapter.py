# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.FixedTimeLocationAdapter import TimeLocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.TimeLocations.RegularDurationMeasurementLocation import \
    RegularDurationMeasurementLocation


class RegularDurationLocationAdapter(TimeLocationAdapter):
    """
    A time location adapter to define a group of locations in a segment.
    The RegularDurationLocationAdapter allows to define n equidistant
    locations on a segment each one separated by a  time delay in ms.
    """

    def __init__(self):
        TimeLocationAdapter.__init__(self)

        self.name = self.tr(u'Regular Duration')

        self._settings.extend([{u'name': unicode(self.tr(u'duration (ms)')), u'type': u'int',
                                u'value': 100, u'step': 1, u'limits': (1, 100000)},
                               {u'name': unicode(self.tr(u'max intervals')), u'type': u'int',
                                u'value': 20, u'step': 1, u'limits': (1, 100000)}])

        # the separation time between locations
        self.duration_ms = 100

        # the max amount of locations (the real amount of locations depends of the segment duration)
        self.max_intervals = 20

        self.settings = Parameter.create(name=u'Time Location', type=u'group', children=self._settings)

    def get_instance(self):
        TimeLocationAdapter.update_instance_variables(self)

        try:
            duration_ms = self.settings.param(unicode(self.tr(u'duration (ms)'))).value()
            max_intervals = self.settings.param(unicode(self.tr(u'max intervals'))).value()

        except Exception as e:
            duration_ms, max_intervals = 100, 100

        self.duration_ms, self.max_intervals = duration_ms, max_intervals

        return [RegularDurationMeasurementLocation(self.duration_ms, i, NFFT=self.fft_points, overlap=self.overlap)
                for i in xrange(self.max_intervals)]