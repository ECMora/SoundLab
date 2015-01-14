from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from graphic_interface.Settings.WorkTheme import WorkTheme, OscillogramTheme, SpectrogramTheme, OneDimensionalTheme, \
    DetectionTheme


_winFuncs = {'Bartlett': WindowFunction.Bartlett,
             'Blackman': WindowFunction.Blackman,
             'Hamming': WindowFunction.Hamming,
             'Hanning': WindowFunction.Hanning,
             'Kaiser': WindowFunction.Kaiser,
             'Rectangular': WindowFunction.Rectangular,
             'None': WindowFunction.WindowNone}

_winFuncs_inv = {value: key for key, value in _winFuncs.iteritems()}


class OscillogramWorkspace(object):
    def __init__(self, minY=-1.0, maxY=1.0, theme=None):
        """

        :param minY: between -1 and 0
        :param maxY: between 0 and 1
        :param theme:
        :return:
        """
        self.minY = minY
        self.maxY = maxY
        self.theme = theme if theme else OscillogramTheme()

    def copy(self):
        return OscillogramWorkspace(self.minY, self.maxY, self.theme.copy())


class SpectrogramWorkspace(object):
    def __init__(self, minY=0, maxY=22050, FFTSize=512, FFTWindow=WindowFunction.Hanning, FFTOverlap=-1,
                 theme=None):
        """

        :param minY: in Hz
        :param maxY: in Hz
        :param FFTSize:
        :param FFTWindow: the value passed must be a function (one of the values of the _winFuncs dictionary),
                          the value stored is the corresponding string
        :param FFTOverlap: between 0 and 1
        :param theme:
        """
        self.minY = minY
        self.maxY = maxY
        self.FFTSize = FFTSize
        self.FFTWindow = FFTWindow
        self.FFTOverlap = FFTOverlap
        self.theme = theme if theme else SpectrogramTheme()

    @property
    def FFTWindow(self):
        return _winFuncs[self._FFTWindow]

    @FFTWindow.setter
    def FFTWindow(self, value):
        self._FFTWindow = _winFuncs_inv[value]

    def copy(self):
        return SpectrogramWorkspace(self.minY, self.maxY, self.FFTSize, self.FFTWindow, self.FFTOverlap,
                                    self.theme.copy())


class OneDimensionalWorkspace(object):
    def __init__(self, theme=None):
        self.theme = theme if theme else OneDimensionalTheme()

    def copy(self):
        return OneDimensionalWorkspace(self.theme.copy())


class DetectionWorkspace(object):
    def __init__(self, theme=None):
        self.theme = theme if theme else DetectionTheme()

    def copy(self):
        return DetectionWorkspace(self.theme.copy())


class Workspace(object):
    def __init__(self, oscillogramWorkspace=None, spectrogramWorkspace=None, oneDimensionalWorkspace=None,
                 detectionWorkspace=None, openedFile=None):
        self.oscillogramWorkspace = oscillogramWorkspace if oscillogramWorkspace else OscillogramWorkspace()
        self.spectrogramWorkspace = spectrogramWorkspace if spectrogramWorkspace else SpectrogramWorkspace()
        self.oneDimensionalWorkspace = oneDimensionalWorkspace if oneDimensionalWorkspace else OneDimensionalWorkspace()
        self.detectionWorkspace = detectionWorkspace if detectionWorkspace else DetectionWorkspace()
        self.openedFile = openedFile

    def copy(self):
        return Workspace(self.oscillogramWorkspace.copy(), self.spectrogramWorkspace.copy(),
                         self.oneDimensionalWorkspace.copy(), self.detectionWorkspace.copy())

    @property
    def workTheme(self):
        return WorkTheme(self.oscillogramWorkspace.theme, self.spectrogramWorkspace.theme,
                         self.oneDimensionalWorkspace.theme, self.detectionWorkspace.theme)

    @workTheme.setter
    def workTheme(self, theme):
        self.oscillogramWorkspace.theme = theme.oscillogramTheme
        self.spectrogramWorkspace.theme = theme.spectrogramTheme
        self.oneDimensionalWorkspace.theme = theme.oneDimensionalTheme
        self.detectionWorkspace.theme = theme.detectionTheme
