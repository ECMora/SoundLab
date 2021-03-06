from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from duetto.dimensional_transformations.one_dimensional_transforms.LogarithmicPowSpectrumTransform import LogarithmicPowSpec
from graphic_interface.one_dimensional_transforms.OneDimensionalHandler import OneDimensionalHandler


class LogarithmicPowSpecHandler(OneDimensionalHandler):
    def __init__(self, parent):
        OneDimensionalHandler.__init__(self, parent)
        self._transform_class = LogarithmicPowSpec

    def get_transform_class(self):
        return self._transform_class

    def get_transform_instance(self):
        return self._transform_class()

    def get_settings(self, transform):
        """

        :type transform: LogarithmicPowSpec
        """
        return [     {u'name': unicode(self.tr(u'FFT window')), u'type': u'list',
                      u'value': transform.window, u'default': WindowFunction.Rectangular,
                      u'values': [(u'Bartlett', WindowFunction.Bartlett),
                                  (u"Blackman", WindowFunction.Blackman),
                                  (u"Hamming", WindowFunction.Hamming),
                                  (u"Hanning", WindowFunction.Hanning),
                                  (u'Kaiser', WindowFunction.Kaiser),
                                  (unicode(self.tr(u'None')), WindowFunction.WindowNone),
                                  (u"Rectangular", WindowFunction.Rectangular)]}]

    def get_axis_labels(self):
        return {u'X': u'Frequency (kHz)', u'Y': u'Intensity (dB)' }

    def get_default_lines(self):
        return True

    def get_y_default(self, transform):
        """

        :type transform: LogarithmicPowSpec
        """
        return (-40, 0)

    def get_y_limits(self,transform):
        """

        :type transform: LogarithmicPowSpec
        """
        return (-50, 0)

    def apply_settings_change(self, transform, change):
        """

        :type transform: LogarithmicPowSpec
        """
        childName, _change, data = change

        if childName == unicode(self.tr(u'FFT window')):
            transform.window = data
