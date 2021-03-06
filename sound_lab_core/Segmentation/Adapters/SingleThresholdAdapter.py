# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sound_lab_core.Segmentation.Adapters.ThresholdAdapter import ThresholdAdapter
from sound_lab_core.Segmentation.OneDimensional.ThresholdDetectors.SingleThresholdDetector import \
    SingleThresholdDetector


class SingleThresholdAdapter(ThresholdAdapter):
    """
    """

    def __init__(self):
        ThresholdAdapter.__init__(self)
        self.name = u'Single Threshold'

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=self.settings_parameter_list)

    def restore_settings(self, adapter_copy, signal):
        if not isinstance(adapter_copy, SingleThresholdAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.get_instance(signal)

        self.settings.param(unicode(self.tr(u'Threshold (dB)'))).setValue(adapter_copy.threshold_dB)
        self.settings.param(unicode(self.tr(u'Min Size (ms)'))).setValue(adapter_copy.min_size_ms)
        self.settings.param(unicode(self.tr(u'Merge Factor (%)'))).setValue(adapter_copy.merge_factor)
        self.settings.param(unicode(self.tr(u'Envelope Type'))).setValue(adapter_copy.envelope)

    def get_instance(self, signal):
        """
        Gets a new get_instance of the corresponding parameter measurement.
        :return: A new get_instance of the corresponding parameter measurement class
        """
        self.update_variables(signal)

        return SingleThresholdDetector(signal, self.threshold_dB, self.min_size_ms, self.merge_factor, self.envelope)