# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.Segmentation.OneDimensional.ThresholdDetectors.TripleThresholdDetector import \
    TripleThresholdDetector
from sound_lab_core.Segmentation.Adapters.ThresholdAdapter import ThresholdAdapter


class TripleThresholdAdapter(ThresholdAdapter):
    """
    Adapter class for the start time parameter.
    """

    # region CONSTANTS

    THRESHOLD2_DEFAULT = -40
    THRESHOLD3_DEFAULT = -40

    # endregion

    def __init__(self):
        ThresholdAdapter.__init__(self)

        self.name = u'Triple Threshold'

        self.settings_parameter_list.insert(1, {u'name': unicode(self.tr(u'Threshold2 (dB)')), u'type': u'float',
                                                u'value': self.THRESHOLD2_DEFAULT,
                                                u'step': 1, u'limits': (-120, 0)})
        self.settings_parameter_list.insert(2, {u'name': unicode(self.tr(u'Threshold3 (dB)')), u'type': u'float',
                                                u'value': self.THRESHOLD3_DEFAULT,
                                                u'step': 1, u'limits': (-120, 0)})

        self.threshold2_dB = self.THRESHOLD2_DEFAULT
        self.threshold3_dB = self.THRESHOLD3_DEFAULT

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=self.settings_parameter_list)

    def restore_settings(self, adapter_copy, signal):
        if not isinstance(adapter_copy, TripleThresholdAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.get_instance(signal)

        self.settings.param(unicode(self.tr(u'Threshold (dB)'))).setValue(adapter_copy.threshold_dB)
        self.settings.param(unicode(self.tr(u'Threshold2 (dB)'))).setValue(adapter_copy.threshold2_dB)
        self.settings.param(unicode(self.tr(u'Threshold3 (dB)'))).setValue(adapter_copy.threshold3_dB)

        self.settings.param(unicode(self.tr(u'Min Size (ms)'))).setValue(adapter_copy.min_size_ms)
        self.settings.param(unicode(self.tr(u'Merge Factor (%)'))).setValue(adapter_copy.merge_factor)
        self.settings.param(unicode(self.tr(u'Envelope Type'))).setValue(adapter_copy.envelope)

    def get_instance(self, signal):
        """
        Gets a new get_instance of the corresponding parameter measurement.
        :return: A new get_instance of the corresponding parameter measurement class
        """

        self.update_variables(signal)

        try:
            threshold2 = self.settings.param(unicode(self.tr(u'Threshold2 (dB)'))).value()
            threshold3 = self.settings.param(unicode(self.tr(u'Threshold3 (dB)'))).value()

        except Exception as ex:
            threshold2, threshold3 = self.THRESHOLD2_DEFAULT, self.THRESHOLD3_DEFAULT

        self.threshold2_dB = threshold2
        self.threshold3_dB = threshold3

        return TripleThresholdDetector(signal, self.threshold_dB, self.threshold2_dB, self.threshold3_dB,
                                       self.min_size_ms, self.merge_factor, self.envelope)