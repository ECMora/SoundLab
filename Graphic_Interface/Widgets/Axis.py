from PyQt4.QtGui import QFont
import pyqtgraph as pg, numpy as np


class OscXAxis(pg.AxisItem):
    def __init__(self, parent, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.parent = parent
        self.setLabel(text="Time (s)")
        font = QFont(self.font)
        font.setPointSize(8)
        self.setTickFont(font)

    def tickStrings(self, values, scale, spacing):
        strns = []
        delta = spacing / self.parent.signalProcessor.signal.samplingRate
        a = max(-(int(np.log10(delta)) - 1), 0)
        a = min(a, 4)
        s = "{:." + str(a) + "f}"
        for x in values:
            strns.append(s.format(x * 1.0 / self.parent.signalProcessor.signal.samplingRate))
        return strns

    def tickValues(self, minVal, maxVal, size):
        minVal = self.parent.mainCursor.min
        maxVal = self.parent.mainCursor.max
        spacing = self.tickSpacing(minVal, maxVal, size)[0][0]
        values = []
        temp = minVal
        while (temp < maxVal):
            values.append(temp)
            temp += spacing
        return [(spacing, values)]

    def tickSpacing(self, minVal, maxVal, size):
        minVal = self.parent.mainCursor.min
        maxVal = self.parent.mainCursor.max
        return [(max((maxVal - minVal) / (10.0 * self.parent.signalProcessor.signal.samplingRate),
                     0.0001) * self.parent.signalProcessor.signal.samplingRate, 0)]


class OscYAxis(pg.AxisItem):
    def __init__(self, parent, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.parent = parent
        self.setLabel(text="Amplitude (%)")
        font = QFont(self.font)
        font.setPointSize(8)
        self.setTickFont(font)

    def tickStrings(self, values, scale, spacing):
        strns = []
        for x in values:
            strns.append("{:.0f}".format(x * 100.0 / self.parent.signalProcessor.signal.getMaximumValueAllowed()))
        return strns


class SpecYAxis(pg.AxisItem):
    def __init__(self,parent,*args,**kwargs):
        pg.AxisItem.__init__(self,*args,**kwargs)
        self.parent = parent;
        self.setLabel(text="Frequency (KHz)")
    def tickStrings(self, values, scale, spacing):
        self.freqs = self.parent.parent().specgramSettings.freqs
        if self.freqs is None:
            return values
        r = self.freqs[[x for x in values if x < len(self.freqs)]]
        for i in range(len(r)):
            r[i] = "{:.1f}".format(r[i]/1000.0)
        return r