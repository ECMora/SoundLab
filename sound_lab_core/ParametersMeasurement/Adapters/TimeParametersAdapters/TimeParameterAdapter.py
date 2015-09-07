# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter

from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter


class TimeParameterAdapter(ParameterAdapter):
    """
    Adapter class for the start time parameter.
    """
    DEFAULT_DECIMAL_PLACES = 3

    def __init__(self):
        ParameterAdapter.__init__(self)
        self._settings = [
            {u'name': unicode(self.tr(u'Decimal Places')), u'type': u'int', u'value': self.DEFAULT_DECIMAL_PLACES
             , u'step': 1, u'limits': (1, 5)}]

        self.decimal_places = self.DEFAULT_DECIMAL_PLACES

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=self._settings)
        self.settings.sigTreeStateChanged.connect(lambda changes: self.dataChanged.emit())

    def state(self):
        self.compute_settings()
        return {"decimals": self.decimal_places}

    def load_state(self, state):
        if "decimals" in state:
            self.settings.param(unicode(self.tr(u'Decimal Places'))).setValue(state["decimals"])

    def get_settings(self):
        return self.settings

    def compute_settings(self):
        # use a try catch because the instance must be required after
        # param tree object is destroyed
        try:
            decimals = self.settings.param(unicode(self.tr(u'Decimal Places'))).value()

        except Exception as e:
            decimals = self.DEFAULT_DECIMAL_PLACES

        if self.decimal_places != decimals:
            self.decimal_places = decimals
