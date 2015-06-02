# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSignal
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.FixedTimeLocationAdapter import LocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.SpectralLocations.FrequencyMeasurementLocation import \
    FrequencyMeasurementLocation


class FrequencyMeasurementLocationAdapter(LocationAdapter):

    # signal raised when there is selected the options of share all spectral locations
    # that means that all spectral locations must be equals
    # raise the adapter in which the share change and the bool of if needs to share its values
    allLocationsSharedChanged = pyqtSignal(object, bool)

    def __init__(self):
        LocationAdapter.__init__(self)

        settings = [{u'name': unicode(self.tr(u'Min Limit(kHz)')), u'type': u'int',
                     u'value': 0, u'step': 1, u'limits': (0, 250)},
                    {u'name': unicode(self.tr(u'Max Limit(kHz)')), u'type': u'int',
                     u'value': 250, u'step': 1, u'limits': (0, 250)},
                    {u'name': unicode(self.tr(u'Intervals')), u'type': u'int',
                     u'value': 1, u'step': 1, u'limits': (1, 1000)},
                    {u'name': unicode(self.tr(u'Share All Locations')), u'type': u'bool',
                     u'value': False}
                    ]

        self.min_limit_kHz = 0
        self.max_limit_kHz = 250
        self.frequency_intervals = 1
        self._shared_locations = False

        self.settings = Parameter.create(name=u'Spectral Location', type=u'group', children=settings)

        self.settings.sigTreeStateChanged.connect(self.check_shared_locations_settings)

    @property
    def shared_locations(self):
        return self._shared_locations

    @shared_locations.setter
    def shared_locations(self, value):
        if self.settings.param(unicode(self.tr(u'Share All Locations'))).value() != value:
            self.settings.param(unicode(self.tr(u'Share All Locations'))).setValue(value)

        self._shared_locations = value

    def check_shared_locations_settings(self):
        shared_locations = self.settings.param(unicode(self.tr(u'Share All Locations'))).value()
        self.allLocationsSharedChanged.emit(self, shared_locations)

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
            _shared_locations = self.settings.param(unicode(self.tr(u'Share All Locations'))).value()

        except Exception as e:
            min_limit_kHz, max_limit_kHz = self.min_limit_kHz, self.max_limit_kHz
            frequency_intervals = self.frequency_intervals

        self.min_limit_kHz = min_limit_kHz
        self.max_limit_kHz = max_limit_kHz
        self.frequency_intervals = frequency_intervals
        self._shared_locations = _shared_locations

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

    def restore_settings(self, adapter_copy, signal=None):
        if not isinstance(adapter_copy, FrequencyMeasurementLocationAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.update_instance_variables()
        self.settings.param(unicode(self.tr(u'Min Limit(kHz)'))).setValue(adapter_copy.min_limit_kHz)
        self.settings.param(unicode(self.tr(u'Max Limit(kHz)'))).setValue(adapter_copy.max_limit_kHz)
        self.settings.param(unicode(self.tr(u'Intervals'))).setValue(adapter_copy.frequency_intervals)
        self.settings.param(unicode(self.tr(u'Share All Locations'))).setValue(adapter_copy.shared_locations)






