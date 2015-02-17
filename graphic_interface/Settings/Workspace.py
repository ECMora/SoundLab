import os
from PyQt4.QtGui import QTabWidget
from duetto.dimensional_transformations.two_dimensional_transforms.Spectrogram.WindowFunctions import WindowFunction
from graphic_interface.settings.WorkTheme import WorkTheme, OscillogramTheme, SpectrogramTheme, OneDimensionalTheme, \
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
    def __init__(self, minY=-100.0, maxY=100.0, theme=None):
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
    def __init__(self, minY=0, maxY=44100, FFTSize=512, FFTWindow=WindowFunction.Hanning, FFTOverlap=-1,
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
    """

    """
    # CONSTANTS
    LAST_OPENED_FILES_AMOUNT = 5

    def __init__(self, oscillogramWorkspace=None, spectrogramWorkspace=None, oneDimensionalWorkspace=None,
                 detectionWorkspace=None, openedFiles=None):
        self.oscillogramWorkspace = oscillogramWorkspace if oscillogramWorkspace else OscillogramWorkspace()
        self.spectrogramWorkspace = spectrogramWorkspace if spectrogramWorkspace else SpectrogramWorkspace()
        self.oneDimensionalWorkspace = oneDimensionalWorkspace if oneDimensionalWorkspace else OneDimensionalWorkspace()
        self.detectionWorkspace = detectionWorkspace if detectionWorkspace else DetectionWorkspace()
        self.openedFiles = [] if openedFiles is None else openedFiles
        self.recentFiles = []

        self.language = u""
        self.theme_file = u""
        self.style = u""

        self.visibleOscilogram = True
        self.visibleSpectrogram = True

        self.tabPosition = int(QTabWidget.North)
        self.tabShape = int(QTabWidget.Rounded)

    @property
    def lastOpenedFolder(self):
        """
        :return: The folder of the last opened file if any else ""
        """
        if self.lastOpenedFile != "":
            return os.path.split(self.lastOpenedFile)[0]
        return ""

    @property
    def lastOpenedFile(self):
        """
        :return: the last opened file path if any.
        """
        # use the recent files to save the state of last opened file
        # after application closed and start again
        return self.recentFiles[-1] if len(self.recentFiles) > 0 else u""

    def clearOpenedFiles(self):
        """
        Clears the last opened files
        :return:
        """
        self.openedFiles = []

    def setClosedFile(self, file_path):
        """
        Update the state of the signal at file_path to close by the application
        If the signal at file_path was previously opened the removes it from
        the list of opened files, otherwise nothing is do it.
        :param file_path: the signal path previously open.
        :return:
        """
        file_path = unicode(file_path)
        if file_path in self.openedFiles:
            self.openedFiles.remove(file_path)

    def addOpenedFile(self, filepath):
        """
        Add a file path to the list of last opened files
        :param filepath:
        :return:
        """
        filepath = unicode(filepath)

        if filepath not in self.openedFiles:
            self.openedFiles.append(filepath)

        if len(self.recentFiles) < self.LAST_OPENED_FILES_AMOUNT:
            self.recentFiles.append(str(filepath))
        else:
            self.recentFiles.append(str(filepath))
            self.recentFiles.pop(0)

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
