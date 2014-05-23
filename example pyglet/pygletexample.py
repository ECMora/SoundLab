# -*- coding: utf-8 -*-
"""
Demonstrates basic use of LegendItem
"""
from PyQt4.QtGui import QFont

import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui



class OscXAxis(pg.AxisItem):
    def __init__(self, parent, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.parent = parent
        font = QFont(self.font)
        font.setPointSize(20)
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


def getImage(widget):
    image = QtGui.QPixmap.grabWindow(widget.winId())
    image.save("Local.jpg", 'jpg')

if __name__ == '__main__':
    import sys

    plt = pg.plot( axisItems={'bottom':  OscXAxis(None, orientation='bottom'), 'left':OscXAxis(None, orientation='left') })
    font = QFont()
    font.setPointSize(15)
    ax = plt.plotItem.getAxis('bottom')
    ax.setTickFont(font)
    ax.setLabel(text="<h1>Time (ms)</h1>")
    ax = plt.plotItem.getAxis('left')
    ax.setTickFont(font)
    plt.setWindowTitle('')
    #plt.addLegend()
    plt.plotItem.showGrid(True,True)


    local_max_match = [95.39, 91.01, 98.67, 96.21, 86.42, 100, 91.53, 88.0, 93.73, 87.5, 90.63, 84.07, 86.46, 71.73, 91.12, 98.78, 71, 86.67, 91.14, 80.15, 99.47, 88.41, 94.69, 98.47, 99.76, 96.26, 99.08, 100, 72.16, 94.31]

    local_max_error =  [0.95, 2.85, 7.09, 0.63, 3.04, 17.86, 6.38, 10.7, 0.86, 18.38, 1.59, 6.44, 3.02, 0.12, 0.12, 0.63, 0, 0, 0.41, 0, 2.37, 0.01, 4.81, 4.06, 0.01, 1.68, 4.2, 10.35, 0.68, 4.09]

    interval_match = [90.51, 84.46, 100, 100, 96.46, 94.61, 97.24, 100, 98.1, 65.81, 80.02, 80.74, 92.11, 60.71, 91.25, 99.67, 72.64, 96.3, 84.85, 82.17, 81.74, 83.88, 69, 82.4, 99.75, 88.71, 98.73, 100, 71.3, 95.97]

    interval_error =[2.86, 6.29, 19.53, 6.06, 12.78, 9.35, 39.28, 32, 2.15, 36.52, 5.58, 29.83, 16.22, 0, 6.55, 1.48, 0.01, 1.41, 0.47, 0.03, 2.99, 0, 0.7, 0.38, 0.15, 3.78, 4.44, 11.28, 0.23, 0]

    envelope_match = [98.03, 96.34, 99.78, 100, 93.48, 100, 98.74, 98.67, 99.83, 96.74, 99.95, 85.45, 92.16, 84.51, 95.52, 99.64, 97.61, 97.74, 96.87, 86.63, 99.47, 93.65, 95.7, 97, 99.79, 95.84, 99.65, 100, 73.63, 93.75]

    envelope_error =[1.54, 7.51, 13.18, 3.38, 4.7, 17.86, 16.96, 24.22, 2.3, 18.93, 3.93, 5.91, 6.77, 0.14, 2.21, 0.95, 0.3, 0, 0.47, 0, 5.68, 0.01, 3.29, 1.49, 0, 0.92, 6, 11.45, 0.09, 3.93]

    intervals_analysis_bats_match = [98.99, 99.2, 99.25, 98.75, 98.84, 98.84, 99.14, 98.96, 98.96, 98.91, 98.79, 98.14, 98.64, 98.46, 97.43, 97.88, 98.5, 97.78, 98.02, 98.67]

    intervals_analysis_bats_error =[8.18, 11.26, 15.67, 19.56, 23.66, 23.66, 34.55, 38.46, 38.46, 48.42, 51.27, 58.74, 61.18, 69.19, 71.27, 79.47, 84.93, 96.47, 118.8, 157.81]

    intervals_analysis_birds_match = [80.95,98.69,90.82,99.15,99.15,99.13,99.11,99.12,99.10,80.04]

    intervals_analysis_birds_error =[27.82,8.97,1.66,9.28,9.28,9.85,9.43,9.71,10.07,0.44]

    #a  = []
    #for x in range(1,len(intervals_analysis_birds_match)+1):
    #    a.append(intervals_analysis_birds_match[x-1])
    #    a.append((intervals_analysis_birds_match[x-1]+intervals_analysis_birds_match[x])/2.0)

    print(len(a))
    rang = np.arange(1,31)

    plt.setRange(xRange=(0,30),
                                         yRange=(-1,110))


    l = pg.LegendItem()  # args are (size, offset)
    l.setParentItem(plt.graphicsItem())   # Note we do NOT call plt.addItem in this case


    #
    #LocalMaxMatch= plt.plot(rang,local_max_match, pen='g', name='Match % ',symbol='o',symbolPen='0F0',symbolBrush='AAA')
    #LocalMaxError = plt.plot(rang,local_max_error, pen='r', name='Difference % ',symbol='o',symbolPen='F00',symbolBrush='AAA')
    #l.addItem(LocalMaxMatch,u"<h1> Local Max Method Match %</h1>")
    #l.addItem(LocalMaxError,u"<h1> Local Max Method Difference %</h1>")

    #IntervalMatch = plt.plot(rang,interval_match, pen='g', name=' Match %',symbol='o',symbolPen='0F0',symbolBrush='AAA')
    #IntervalError = plt.plot(rang,interval_error, pen='r', name=' Difference %',symbol='o',symbolPen='F00',symbolBrush='AAA')
    #l.addItem(IntervalMatch,u"<h1> Interval RMS Method Match %</h1>")
    #l.addItem(IntervalError,u"<h1> Interval RMS Method Difference %</h1>")

    #EnvelopeMatch = plt.plot(rang,envelope_match, pen='g', name='Match %',symbol='o',symbolPen='0F0',symbolBrush='AAA')
    #EnvelopeError= plt.plot(rang,envelope_error, pen='r', name='Difference %',symbol='o',symbolPen='F00',symbolBrush='AAA')
    #l.addItem(EnvelopeMatch,u"<h1> Envelope Method Match %</h1>")
    #l.addItem(EnvelopeError,u"<h1>Envelope Method Difference %</h1>")

    #
    #rang = np.arange(1,len(intervals_analysis_bats_match)+1)
    #rang = rang/2.0
    #plt.setRange(xRange=(0,rang.size/2),yRange=(0,120))
    #Intervals_Analysis_Bats_Match = plt.plot(rang,intervals_analysis_bats_match, pen='g', name='Match %',symbol='o',symbolPen='0F0',symbolBrush='AAA')
    #Intervals_Analysis_Bats_Error= plt.plot(rang,intervals_analysis_bats_error, pen='r', name='Difference %',symbol='o',symbolPen='F00',symbolBrush='AAA')
    #l.addItem(Intervals_Analysis_Bats_Match,u"<h1> Interval RMS (Bats) Match%</h1>")
    #l.addItem(Intervals_Analysis_Bats_Error,u"<h1>Interval RMS (Bats) Difference %</h1>")

    rang = np.arange(1,len(intervals_analysis_birds_match)+1)
    plt.setRange(xRange=(0,rang.size),yRange=(0,120))
    Intervals_Analysis_Birds_Match = plt.plot(rang,intervals_analysis_birds_match, pen='g', name='Match %',symbol='o',symbolPen='0F0',symbolBrush='AAA')
    Intervals_Analysis_Birds_Error= plt.plot(rang,intervals_analysis_birds_error, pen='r', name='Difference %',symbol='o',symbolPen='F00',symbolBrush='AAA')
    l.addItem(Intervals_Analysis_Birds_Match,u"<h1> Interval RMS (Birds) Match%</h1>")
    l.addItem(Intervals_Analysis_Birds_Error,u"<h1>Interval RMS (Birds) Difference %</h1>")



    ## Start Qt event loop unless running in interactive mode or using pyside.

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):

        getImage(plt)

        QtGui.QApplication.instance().exec_()
