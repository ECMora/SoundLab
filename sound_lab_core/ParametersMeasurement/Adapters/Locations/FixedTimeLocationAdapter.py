# -*- coding: utf-8 -*-
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter


class FixedTimeLocationAdapter(SoundLabAdapter):
    def __init__(self):
        SoundLabAdapter.__init__(self)

        settings = [{u'name': unicode(self.tr(u'ms delay')), u'type': u'int',
                     u'value': 0, u'step': 1, u'limits': (0, 60 * 60 * 1000)}]  # 1 hour segment as upper limit

        self.ms_delay = 0

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def update_instance_variables(self):
        """

        :return:
        """
        try:
            ms_delay = self.settings.param(unicode(self.tr(u'ms delay'))).value()

        except Exception as e:
            ms_delay = 0

        self.ms_delay = ms_delay

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings


