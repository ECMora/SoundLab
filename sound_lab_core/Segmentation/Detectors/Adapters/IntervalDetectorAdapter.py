# -*- coding: utf-8 -*-
from sound_lab_core.SoundLabAdapter import SoundLabAdapter
from pyqtgraph.parametertree import Parameter
from utils.Utils import fromdB
import pyqtgraph as pg


class IntervalDetectorAdapter(SoundLabAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

        settings = [
            {u'name': unicode(self.tr(u'Threshold (dB)')), u'type': u'float', u'value': -20.00, u'step': 1, u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Threshold Start(dB)')), u'type': u'int', u'value': 0.00, u'step': 1,
             u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Threshold End(dB)')), u'type': u'int', u'value': 0.00, u'step': 1,
             u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Min Size (ms)')), u'type': u'float', u'value': 2.00, u'step': 1, u'limits': (0, 30000)},
            {u'name': unicode(self.tr(u'Merge Factor (%)')), u'type': u'int', u'value': 5.00, u'step': 1,
             u'limits': (0, 50)}]

        self.threshold_dB = -20
        self.min_size_ms = 2
        self.merge_factor = 5
        self.threshold2_dB = 0
        self.threshold3_dB = 0

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

        # visual items
        # the time region limits
        self.threshold_line_item = pg.InfiniteLine(angle=0, pos=2000, movable=True,
                                                   pen=pg.mkPen(color=self.COLOR, width=self.VISUAL_ITEM_LINE_WIDTH))

        self.signal_max_value = 2 ** 16
        self.settings.param(unicode(self.tr(u'Threshold (dB)'))).sigValueChanged.connect(
            lambda parameter: self.threshold_line_item.setValue(fromdB(parameter.value(), 0, self.signal_max_value)))

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings

    def update_instance_variables(self):
        """
        Gets a new get_instance of the corresponding parameter measurement.
        :return: A new get_instance of the corresponding parameter measurement class
        """
        try:
            threshold = self.settings.param(unicode(self.tr(u'Threshold (dB)'))).value()
            min_size = self.settings.param(unicode(self.tr(u'Min Size (ms)'))).value()
            merge_factor = self.settings.param(unicode(self.tr(u'Merge Factor (%)'))).value()
            threshold2 = self.settings.param(unicode(self.tr(u'Threshold Start(dB)'))).value()
            threshold3 = self.settings.param(unicode(self.tr(u'Threshold End(dB)'))).value()

        except Exception as ex:
            threshold, threshold2, threshold3 = -20, 0, 0
            min_size, merge_factor = 2, 5

        self.threshold_dB = threshold
        self.min_size_ms = min_size
        self.merge_factor = merge_factor
        self.threshold2_dB = threshold2
        self.threshold3_dB = threshold3

    def restore_settings(self, adapter_copy, signal):
        if not isinstance(adapter_copy, SoundLabAdapter) or \
                not isinstance(adapter_copy, IntervalDetectorAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.get_instance(signal)
        self.settings.param(unicode(self.tr(u'Threshold (dB)'))).setValue(adapter_copy.threshold_dB)
        self.settings.param(unicode(self.tr(u'Threshold Start(dB)'))).setValue(adapter_copy.threshold2_dB)
        self.settings.param(unicode(self.tr(u'Threshold End(dB)'))).setValue(adapter_copy.threshold3_dB)
        self.settings.param(unicode(self.tr(u'Min Size (ms)'))).setValue(adapter_copy.min_size_ms)
        self.settings.param(unicode(self.tr(u'Merge Factor (%)'))).setValue(adapter_copy.merge_factor)

    def get_visual_items(self):
        return [self.threshold_line_item]