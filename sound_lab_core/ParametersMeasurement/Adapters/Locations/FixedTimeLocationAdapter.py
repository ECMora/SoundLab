# -*- coding: utf-8 -*-
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter


class LocationAdapter(SoundLabAdapter):
    def __init__(self):
        SoundLabAdapter.__init__(self)

    def get_instance(self):
        """
        The location adapter returns a list with all the locations
        that the adapter is managing. A single adapter could manage
        multiple locations of a same type. Example: Segment x-distant
        divided by n then return n locations
        :return:
        """
        return []


class FixedTimeLocationAdapter(LocationAdapter):

    def __init__(self):
        LocationAdapter.__init__(self)

        settings = [{u'name': unicode(self.tr(u'ms delay')), u'type': u'int',
                     u'value': 0, u'step': 1, u'limits': (0, 60 * 60 * 1000)},
                    {u'name': unicode(self.tr(u'min limit kHz')), u'type': u'int',
                     u'value': 0, u'step': 1, u'limits': (0, 250)},
                    {u'name': unicode(self.tr(u'max limit kHz')), u'type': u'int',
                     u'value': 250, u'step': 1, u'limits': (0, 250)},
                    {u'name': unicode(self.tr(u'Freq interval')), u'type': u'int',
                     u'value': 1, u'step': 1, u'limits': (1, 1000)},
                    ]

        self.ms_delay = 0
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



