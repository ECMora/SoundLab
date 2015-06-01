# -*- coding: utf-8 -*-
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter


class LocationAdapter(SoundLabAdapter):
    def __init__(self):
        SoundLabAdapter.__init__(self)

        self.settings = Parameter.create(name=u'Time Location', type=u'group', children=[])

    def get_instance(self):
        """
        The location adapter returns a list with all the locations
        that the adapter is managing. A single adapter could manage
        multiple locations of a same type. Example: Segment x-distant
        divided by n then return n locations
        :return:
        """
        return []

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings


class FixedTimeLocationAdapter(LocationAdapter):

    def __init__(self):
        LocationAdapter.__init__(self)

        settings = [{u'name': unicode(self.tr(u'ms delay')), u'type': u'int',
                     u'value': 0, u'step': 1, u'limits': (0, 60 * 60 * 1000)}]

        self.ms_delay = 0

        self.settings = Parameter.create(name=u'Time Location', type=u'group', children=settings)

    def update_instance_variables(self):
        try:
            ms_delay = self.settings.param(unicode(self.tr(u'ms delay'))).value()

        except Exception as e:
            ms_delay = 0

        self.ms_delay = ms_delay