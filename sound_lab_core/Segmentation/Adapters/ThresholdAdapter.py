from sound_lab_core.Segmentation.OneDimensional.DetectionEnvelopes.AbsDecayEnvelope import AbsDecayEnvelope
from sound_lab_core.Segmentation.OneDimensional.DetectionEnvelopes.IntervalMaxEnvelope import IntervalMaxEnvelope
from sound_lab_core.Segmentation.OneDimensional.DetectionEnvelopes.IntervalMaxMeanEnvelope import \
    IntervalMaxMeanEnvelope
from sound_lab_core.Segmentation.OneDimensional.DetectionEnvelopes.IntervalRmsEnvelope import IntervalRmsEnvelope
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class ThresholdAdapter(SoundLabAdapter):
    """
    refactor class for thresholds adapters
    """

    # region CONSTANTS

    THRESHOLD_DEFAULT = -20
    MIN_SIZE_DEFAULT = 1
    MERGE_FACTOR_DEFAULT = 0
    ENVELOPE_DEFAULT = IntervalRmsEnvelope

    # endregion

    def __init__(self):
        SoundLabAdapter.__init__(self)

        self.settings_parameter_list = [
            {u'name': unicode(self.tr(u'Threshold (dB)')), u'type': u'float', u'value': self.THRESHOLD_DEFAULT,
             u'step': 1, u'limits': (-120, 0)},
            {u'name': unicode(self.tr(u'Envelope Type')), u'type': u'list',
             u'value': self.ENVELOPE_DEFAULT,
             u'default': self.ENVELOPE_DEFAULT,
             u'values': [(u'Interval_RMS', IntervalRmsEnvelope),
                         (u"Interval_Max_Mean", IntervalMaxMeanEnvelope),
                         (u"Interval_Local_Max", IntervalMaxEnvelope),
                         (u"Abs_Decay", AbsDecayEnvelope)
             ]},
            {u'name': unicode(self.tr(u'Min Size (ms)')), u'type': u'float', u'value': self.MIN_SIZE_DEFAULT,
             u'step': 1, u'limits': (0, 30000)},
            {u'name': unicode(self.tr(u'Merge Factor (%)')), u'type': u'int', u'value': self.MERGE_FACTOR_DEFAULT,
             u'step': 1, u'limits': (0, 50)}]

        self.threshold_dB = self.THRESHOLD_DEFAULT
        self.min_size_ms = self.MIN_SIZE_DEFAULT
        self.merge_factor = self.MERGE_FACTOR_DEFAULT
        self.envelope = self.ENVELOPE_DEFAULT

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings

    def update_variables(self, signal):
        try:
            threshold = self.settings.param(unicode(self.tr(u'Threshold (dB)'))).value()
            min_size = self.settings.param(unicode(self.tr(u'Min Size (ms)'))).value()
            merge_factor = self.settings.param(unicode(self.tr(u'Merge Factor (%)'))).value()
            envelope = self.settings.param(unicode(self.tr(u'Envelope Type'))).value()

        except Exception as ex:
            threshold, min_size, merge_factor = self.THRESHOLD_DEFAULT, self.MIN_SIZE_DEFAULT, self.MERGE_FACTOR_DEFAULT
            envelope = self.ENVELOPE_DEFAULT

        self.threshold_dB = threshold
        self.min_size_ms = min_size
        self.merge_factor = merge_factor
        self.envelope = envelope(signal, threshold, self.min_size_ms * signal.samplingRate / 1000)
