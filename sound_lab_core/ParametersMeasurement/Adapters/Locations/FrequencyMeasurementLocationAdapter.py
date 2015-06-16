# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSignal
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.LocationAdapter import LocationAdapter
from sound_lab_core.ParametersMeasurement.Locations.SpectralLocations.FrequencyMeasurementLocation import \
    FrequencyMeasurementLocation


class FrequencyMeasurementLocationAdapter(LocationAdapter):
    """
    The adapter to create frequency locations for parameter measurement.
    A frequency location is an spectral region of the segment in which
    the parameter would be computed.

    Example: 10-20 kHz
    """

    # region SIGNALS

    # signal raised when there is selected the options of share all spectral locations
    # that means that all spectral locations must be equals
    # raise the adapter in which the share change and the bool of if needs to share its values
    allLocationsSharedChanged = pyqtSignal(object, bool)

    # endregion

    def __init__(self):
        LocationAdapter.__init__(self)

        settings = [{u'name': unicode(self.tr(u'Min Limit(kHz)')), u'type': u'int',
                     u'value': 0, u'step': 1, u'limits': (0, 250)},

                    {u'name': unicode(self.tr(u'Max Limit(kHz)')), u'type': u'int',
                     u'value': 250, u'step': 1, u'limits': (0, 250)},

                    {u'name': unicode(self.tr(u'Intervals')), u'type': u'int',
                     u'value': 1, u'step': 1, u'limits': (1, 1000)},

                    {u'name': unicode(self.tr(u'Share All Locations')), u'type': u'bool',
                     u'value': False}]

        # limits of frequency measurements
        self.min_limit_kHz = 0
        self.max_limit_kHz = 250

        # how many intervals the range of frequency (min_limit_kHz-max_limit_kHz) would be divided into
        self.frequency_intervals = 1

        # if the frequency locations would be shared by all the parameters
        self._shared_locations = False

        self.settings = Parameter.create(name=u'Spectral Location', type=u'group', children=settings)

        self.settings.sigTreeStateChanged.connect(lambda: self.allLocationsSharedChanged.emit(self,
                                                  self.settings.param(unicode(self.tr(u'Share All Locations'))).value()))

    # region Properties

    @property
    def shared_locations(self):
        return self._shared_locations

    @shared_locations.setter
    def shared_locations(self, value):
        if self.settings.param(unicode(self.tr(u'Share All Locations'))).value() != value:
            self.settings.param(unicode(self.tr(u'Share All Locations'))).setValue(value)

        self._shared_locations = value

    # endregion

    def update_data(self, signal):
        """
        Updates the limits of the frequency range values using the allowed range of the supplied signal
        """

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

    def get_instance(self):
        self.update_instance_variables()

        # the result may be a multiple location objects if the frequency_intervals != 1
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






