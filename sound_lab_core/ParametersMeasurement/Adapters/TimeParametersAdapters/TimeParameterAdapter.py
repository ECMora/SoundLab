# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter

from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter


class TimeParameterAdapter(ParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        ParameterAdapter.__init__(self)
        self._settings = [
            {u'name': unicode(self.tr(u'Decimal Places')), u'type': u'int', u'value': 3, u'step': 1,
             u'limits': (1, 5)}]

        self.decimal_places = 3

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=self._settings)

    def state(self):
        return {"decimals":self.decimal_places}

    def load_state(self, state):
        decimals = state["decimals"] if "decimals" in state else self.decimal_places
        self.settings.param(unicode(self.tr(u'Decimal Places'))).setValue(decimals)

    def get_settings(self):
        return self.settings

    def compute_settings(self):
        # use a try catch because the instance must be required after
        # param tree object is destroyed
        try:
            decimals = self.settings.param(unicode(self.tr(u'Decimal Places'))).value()

        except Exception as e:
            decimals = 3

        self.decimal_places = decimals
