from PyQt4.QtGui import QFont
import pyqtgraph as pg
import numpy as np


class OscXAxis(pg.AxisItem):
    """
    Class that extends the behavior of the pyqtgraph axis
    for the use in the oscilogram widget X axis.
    """

    def __init__(self, parent, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.enableAutoSIPrefix(False)
        font = QFont(self.font)
        font.setPointSize(10)
        self.setTickFont(font)
        # set the axis as not dragables to ignore the drag events
        self.mouseDragEvent = lambda ev: False

    # region Scale
    # Scale property
    # Is the scale relation between the real coordinates and the showed in
    # the axis. Is the parameter to divide for the real scale coordinates.

    def __getScale(self):
        return self.__scale

    def __setScale(self,value):
        self.__scale = value

    scale = property(__getScale,__setScale)
    # endregion

    def tickStrings(self, values, scale, spacing):
        """
        Override method set a custom string in each coordinate label on the axis.
        :param values:
        :param scale:
        :param spacing:
        :return:
        """
        strns = []
        delta = spacing / self.scale
        a = max(-(int(np.log10(delta)) - 1), 0)
        a = min(a, 4)
        s = "{:." + str(a) + "f}"
        for x in values:
            strns.append(s.format(x * 1.0 / self.scale))

        if len(strns) > 0:
            strns[len(strns)/2] = self.tr(u"Time(s)")
        return strns

    def tickValues(self, minVal, maxVal, size):
        spacing = self.tickSpacing(minVal, maxVal, size)[0][0]
        values = []
        temp = minVal
        while temp < maxVal:
            values.append(temp)
            temp += spacing
        return [(spacing, values)]

    def tickSpacing(self, minVal, maxVal, size):
        return [(max((maxVal - minVal) / (10.0 * self.scale),
                     0.0001) * self.scale, 0)]


class OscYAxis(pg.AxisItem):
    """
    Class that extends the behavior of the pyqtgraph axis
    for the use in the oscilogram widget Y axis.
    """
    def __init__(self, parent, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.enableAutoSIPrefix(False)
        font = QFont(self.font)
        font.setPointSize(10)
        self.setTickFont(font)
        self.mouseDragEvent = lambda a: False

    # region Scale
    def __getScale(self):
        return self.__scale

    def __setScale(self,value):
        self.__scale = value

    scale = property(__getScale,__setScale)
    # endregion

    def tickStrings(self, values, scale, spacing):
        """
        Override the visible string for the axis coordinates.
        :param values:
        :param scale:
        :param spacing:
        :return:
        """
        strns = []
        for x in values:
            strns.append("{:.0f}".format(x / self.scale))

        if len(strns) > 2:
            strns[-1] = "%"
            strns[0] = ""

        return strns

    def tickSpacing(self, minVal, maxVal, size):
        return [(max((maxVal - minVal) / (10.0 * self.scale), 0.01) * self.scale, 0)]


class SpecYAxis(pg.AxisItem):
    """
    Class that extends the behavior of the pyqtgraph axis
    for the use in the spectrogram widget Y axis.
    """
    def __init__(self, parent, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)

        # customize the axis for the use on spectrogram
        # customize the y coordinates in terms of frequencies.
        # allowed for the spectrogram
        self.__freqs = []
        self.mouseDragEvent = lambda a: False

    # region frequencies property

    @property
    def frequencies(self):
        return self.__freqs

    @frequencies.setter
    def frequencies(self, freqs):
        self.__freqs = freqs

    # endregion

    def tickStrings(self, values, scale, spacing):
        if len(self.__freqs) == 0:
            return values
        freqs = self.__freqs[[x for x in values if x < len(self.__freqs)]]

        for i in range(len(freqs)):
            freqs[i] = "{:.1f}".format(freqs[i]/1000.0)

        return freqs