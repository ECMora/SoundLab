# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.FixedTimeLocationAdapter import LocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.SpectralLocations.FrequencyMeasurementLocation import \
    FrequencyMeasurementLocation


class FrequencyMeasurementLocationAdapter(LocationAdapter):

    def __init__(self):
        LocationAdapter.__init__(self)

        settings = [{u'name': unicode(self.tr(u'Min Limit(kHz)')), u'type': u'int',
                     u'value': 0, u'step': 1, u'limits': (0, 250)},
                    {u'name': unicode(self.tr(u'Max Limit(kHz)')), u'type': u'int',
                     u'value': 250, u'step': 1, u'limits': (0, 250)},
                    {u'name': unicode(self.tr(u'Intervals')), u'type': u'int',
                     u'value': 1, u'step': 1, u'limits': (1, 1000)},
                    ]

        self.min_limit_kHz = 0
        self.max_limit_kHz = 250
        self.frequency_intervals = 1

        self.settings = Parameter.create(name=u'Spectral Location', type=u'group', children=settings)

    def update_data(self, signal):
        min_kHz, max_kHz = 0, signal.samplingRate / 2000.0

        min_kHz = max(self.min_limit_kHz, min_kHz)
        max_kHz = min(self.max_limit_kHz, max_kHz)

        self.min_limit_kHz, self.max_limit_kHz = min_kHz, max_kHz

        self.settings.param(unicode(self.tr(u'Min Limit(kHz)'))).setLimits((min_kHz, max_kHz))
        self.settings.param(unicode(self.tr(u'Max Limit(kHz)'))).setLimits((min_kHz, max_kHz))

        # updating the values
        min_limit_kHz = self.settings.param(unicode(self.tr(u'Min Limit(kHz)'))).value()
        max_limit_kHz = self.settings.param(unicode(self.tr(u'Max Limit(kHz)'))).value()

        if min_limit_kHz < min_kHz:
            self.settings.param(unicode(self.tr(u'Min Limit(kHz)'))).setValue(min_kHz)

        if max_limit_kHz > max_kHz:
            self.settings.param(unicode(self.tr(u'Max Limit(kHz)'))).setValue(max_kHz)

    def update_instance_variables(self):
        try:
            min_limit_kHz = self.settings.param(unicode(self.tr(u'Min Limit(kHz)'))).value()
            max_limit_kHz = self.settings.param(unicode(self.tr(u'Max Limit(kHz)'))).value()
            frequency_intervals = self.settings.param(unicode(self.tr(u'Intervals'))).value()

        except Exception as e:
            min_limit_kHz, max_limit_kHz = self.min_limit_kHz, self.max_limit_kHz
            frequency_intervals = self.frequency_intervals

        self.min_limit_kHz = min_limit_kHz
        self.max_limit_kHz = max_limit_kHz
        self.frequency_intervals = frequency_intervals

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings

    def get_instance(self):
        self.update_instance_variables()

        locations = []
        freq_step = (self.max_limit_kHz - self.min_limit_kHz) * 1.0 / self.frequency_intervals

        for i in xrange(self.frequency_intervals):
            locations.append(FrequencyMeasurementLocation(int(self.min_limit_kHz + i * freq_step),
                                                          int(self.min_limit_kHz + (i + 1) * freq_step)))

        return locations






