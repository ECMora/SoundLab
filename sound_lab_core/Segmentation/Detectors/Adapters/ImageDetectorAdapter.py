# -*- coding: utf-8 -*-
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter


class ImageDetectorAdapter(SoundLabAdapter):
    """
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

        settings = [
            {u'name': unicode(self.tr(u'Min Size (ms)')), u'type': u'float', u'value': 2.00, u'step': 1, u'limits': (0, 30000)},
            {u'name': unicode(self.tr(u'Min Size (kHz)')), u'type': u'float', u'value': 2.00, u'step': 1, u'limits': (0, 30000)}]

        self.min_size_ms = 2
        self.min_size_kHz = 2

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def update_instance_variables(self):
        """

        :return:
        """
        try:
            min_size_ms = self.settings.param(unicode(self.tr(u'Min Size (ms)'))).value()
            min_size_kHz = self.settings.param(unicode(self.tr(u'Min Size (kHz)'))).value()

        except Exception as e:
            min_size_ms = 2
            min_size_kHz = 2

        self.min_size_ms = min_size_ms
        self.min_size_kHz = min_size_kHz

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings

    def restore_settings(self, adapter_copy, signal):
        if not isinstance(adapter_copy, SoundLabAdapter) or \
                not isinstance(adapter_copy, ImageDetectorAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.get_instance(signal)

        self.settings.param(unicode(self.tr(u'Min Size (ms)'))).setValue(adapter_copy.min_size_ms)
        self.settings.param(unicode(self.tr(u'Min Size (kHz)'))).setValue(adapter_copy.min_size_kHz)
