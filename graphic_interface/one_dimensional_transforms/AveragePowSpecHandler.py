from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from duetto.dimensional_transformations.one_dimensional_transforms.AveragePowSpectrumTransform import AveragePowSpec
from graphic_interface.one_dimensional_transforms.OneDimensionalHandler import OneDimensionalHandler


class AveragePowSpecHandler(OneDimensionalHandler):
    def __init__(self, parent):
        OneDimensionalHandler.__init__(self, parent)
        self._transform_class = AveragePowSpec

    def get_transform_class(self):
        return self._transform_class

    def get_transform_instance(self):
        return self._transform_class()

    def get_settings(self, transform):
        """

        :type transform: AveragePowSpec
        """
        return [            {u'name': unicode(self.tr(u'FFT size')), u'type': u'list', u'default': 512,
                      u'values': [(u"16", 16), (u"32", 32), (u"64", 64), (u"128", 128), (u"256", 256), (u"512", 512), (u"1024", 1024),(u"2048", 2048), (u"4096", 4096), (u"8192", 8192), (u"16384", 16384)],
                      u'value': transform.NFFT},
                     {u'name': unicode(self.tr(u'FFT window')), u'type': u'list',
                      u'value': transform.window, u'default': WindowFunction.Rectangular,
                      u'values': [(u'Bartlett', WindowFunction.Bartlett),
                                  (u"Blackman", WindowFunction.Blackman),
                                  (u"Hamming", WindowFunction.Hamming),
                                  (u"Hanning", WindowFunction.Hanning),
                                  (u'Kaiser', WindowFunction.Kaiser),
                                  (unicode(self.tr(u'None')), WindowFunction.WindowNone),
                                  (u"Rectangular", WindowFunction.Rectangular)]},
                     {u'name': unicode(self.tr(u'FFT overlap')), u'type': u'int', u'limits': (1, 99),
                      u'value': transform.overlapRatio}]

    def get_axis_labels(self):
        return {u'X': u'Frequency (kHz)', u'Y': u'Intensity (dB)' }

    def get_default_lines(self):
        return True

    def get_y_default(self, transform):
        """

        :type transform: AveragePowSpec
        """
        return (-40,0)

    def get_y_limits(self, transform):
        """

        :type transform: AveragePowSpec
        """
        return (-50,0)

    def apply_settings_change(self, transform, change):
        """

        :type transform: AveragePowSpec
        """
        childName, _change, data = change

        if childName == unicode(self.tr(u'FFT window')):
            transform.window = data

        elif childName == unicode(self.tr(u'FFT size')):
            transform.NFFT = data

        elif childName == unicode(self.tr(u'FFT overlap')):
            transform.overlapRatio = data