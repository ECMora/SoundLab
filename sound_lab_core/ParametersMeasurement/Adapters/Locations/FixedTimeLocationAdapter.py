# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.Locations.LocationAdapter import LocationAdapter


class TimeLocationAdapter(LocationAdapter):
    """
    Location adapter for the locations of time, those are the locations that
    define a time piece of the segment to perform the parameter measurements.
    """

    def __init__(self):
        LocationAdapter.__init__(self)

        self._settings = [{u'name': unicode(self.tr(u'FFT points')), u'type': u'int',
                           u'value': 256, u'step': 1, u'limits': (32, 1000000)},
                          {u'name': unicode(self.tr(u'overlap (%)')), u'type': u'int',
                           u'value': 50, u'step': 1, u'limits': (0, 99)}]

        # the time delay in ms of the time location
        self.fft_points = 256
        self.overlap = 50

        self.settings = Parameter.create(name=u'Time Location', type=u'group', children=self._settings)
        self.settings.sigTreeStateChanged.connect(lambda changes: self.dataChanged.emit())

    def update_data(self, NFFT, overlap):
        self.settings.param(unicode(self.tr(u'FFT points'))).setValue(NFFT)
        self.settings.param(unicode(self.tr(u'overlap (%)'))).setValue(overlap)
        self.update_instance_variables()

    def update_instance_variables(self):
        try:
            fft_points = self.settings.param(unicode(self.tr(u'FFT points'))).value()
            overlap = self.settings.param(unicode(self.tr(u'overlap (%)'))).value()

        except Exception as e:
            fft_points, overlap = 256, 50

        self.fft_points = fft_points
        self.overlap = overlap

    def state(self):
        self.update_instance_variables()
        return dict(NFFT=self.fft_points, overlap=self.overlap)

    def load_state(self, state):
        if "NFFT" in state:
            self.settings.param(unicode(self.tr(u'FFT points'))).setValue(state["NFFT"])

        if "overlap" in state:
            self.settings.param(unicode(self.tr(u'overlap (%)'))).setValue(state["overlap"])

        self.update_instance_variables()


class FixedTimeLocationAdapter(TimeLocationAdapter):
    """
    """

    def __init__(self):
        TimeLocationAdapter.__init__(self)

        self._settings.append({u'name': unicode(self.tr(u'ms delay')), u'type': u'int',
                               u'value': 0, u'step': 1, u'limits': (0, 60 * 60 * 1000)})

        # the time delay in ms of the time location
        self.ms_delay = 0

        self.settings = Parameter.create(name=u'Time Location', type=u'group', children=self._settings)
        self.settings.sigTreeStateChanged.connect(lambda changes: self.dataChanged.emit())

    def update_instance_variables(self):
        TimeLocationAdapter.update_instance_variables(self)

        try:
            ms_delay = self.settings.param(unicode(self.tr(u'ms delay'))).value()

        except Exception as e:
            ms_delay = 0

        self.ms_delay = ms_delay

    def state(self):
        self.update_instance_variables()

        parent_state = TimeLocationAdapter.state(self)
        parent_state["ms_delay"] = self.ms_delay
        return parent_state

    def load_state(self, state):
        TimeLocationAdapter.load_state(self, state)

        if "ms_delay" in state:
            self.settings.param(unicode(self.tr(u'ms delay'))).setValue(state["ms_delay"])
            self.ms_delay = state["ms_delay"]
