# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter


class WaveParameterAdapter(ParameterAdapter):
    """
    Adapter class for the Zero cross rate time parameter.
    """

    def __init__(self):
        ParameterAdapter.__init__(self)
        settings = [
            {u'name': unicode(self.tr(u'Decimal Places')), u'type': u'int', u'value': 2, u'step': 1,
             u'limits': (1, 5)}]

        self.decimal_places = 2

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def get_settings(self):
        return self.settings

    def compute_settings(self):
        # use a try catch because the instance must be required after
        # param tree object is destroyed
        try:
            decimals = self.settings.param(unicode(self.tr(u'Decimal Places'))).value()

        except Exception as e:
            decimals = 2

        self.decimal_places = decimals