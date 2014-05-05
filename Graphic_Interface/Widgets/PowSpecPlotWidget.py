from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QCursor
import pyqtgraph as pg
import numpy
from Graphic_Interface.Widgets.Tools import Tools

class PowSpecPlotWidget(pg.PlotWidget):
    def __init__(self,  parent=None,**kargs):
        pg.PlotWidget.__init__(self, **kargs)
        self.mousePressed = False
        self.getPlotItem().setMouseEnabled(x=False, y=False)
        self.xLine = pg.InfiniteLine(angle = 90,pen=(0,9))
        self.yLine = pg.InfiniteLine(angle = 0,pen=(0,9))
        #pointerCursor-----------------------------------
        self.pointerCursor = pg.ScatterPlotItem()
        self.selectedTool = Tools.PointerCursor
        self.getPlotItem().getViewBox().addItem(self.pointerCursor)
        self.getPlotItem().getViewBox().addItem(self.xLine)
        self.getPlotItem().getViewBox().addItem(self.yLine)
        self.mouseReleased = False
        self.last = {}

    PointerChanged = pyqtSignal(str)
    PointerCursorPressed = pyqtSignal()
    PIXELS_OF_CURSORS_CHANGES = 5

    def clearPointerCursor(self):
        self.pointerCursor.clear()
        self.mouseReleased = False

    def mouseMoveEvent(self, event):

        if self.selectedTool == Tools.PointerCursor:
            if self.mousePressed:return

            (x,insidex) = self.fromCanvasToClient(event.x())
            (y,insidey) = self.fromCanvasToClientY(event.y())
            info = self.getFrequencyAmplitudeInfo(x)


            self.xLine.setValue(info[0])
            self.yLine.setValue(info[1])

            if self.mouseReleased:
                 info0 = self.getFrequencyAmplitudeInfo(self.last['pos'][0])
                 self.PointerChanged.emit(str.format('f0: {0}kHz  Amplitude0: {1}dB f1: {2}kHz Amplitude1: {3}dB',numpy.round(info0[0]/1000,1),numpy.round(info0[1],1) ,numpy.round(info[0]/1000,1), numpy.round(info[1],1)))
            else:
                self.PointerChanged.emit(str.format('Frequency: {0}kHz  Amplitude: {1}dB',numpy.round(info[0]/1000,1),numpy.round(info[1],1)))
            if not insidex or not insidey:
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            else:
                self.setCursor(QCursor(QtCore.Qt.BlankCursor))
            self.update()

    def mousePressEvent(self, event):
        self.mousePressed = True
        if self.selectedTool == Tools.PointerCursor:
            self.pointerCursor.clear()
            (x,insidex) = self.fromCanvasToClient(event.x())
            info = self.getFrequencyAmplitudeInfo(x)
            if not insidex:
                self.setCursor(QCursor(QtCore.Qt.BlankCursor))
                return
            self.last = {'pos':[info[0],info[1]], 'pen': {'color': 'w', 'width': 2},'brush':pg.intColor(255, 255), 'symbol':'+', 'size':20}
            self.pointerCursor.addPoints([self.last])
            self.mouseReleased = False
            self.PointerCursorPressed.emit()

    def mouseReleaseEvent(self, event):
        self.mousePressed = False
        if self.selectedTool == Tools.PointerCursor:
            self.mouseReleased = True

    def fromClientToCanvas(self, indexX):
        """
        Translates the index in the signal array to its corresponding coordinates in the canvas
        """
        vb = self.getPlotItem().getViewBox()
        maxx = vb.width()
        a, b = self.getPlotItem().viewRange()[0]
        return int(vb.x() + round((maxx) * (indexX - a) * 1. / (b - a), 0))

    #PIXELS_BETWEEN_AXES_AND_DATA = 10 #the pixels for the numbers in the left side

    def fromCanvasToClientIndex(self, xPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        vb = self.getPlotItem().getViewBox()
        minx = vb.x()
        maxx = vb.width() + minx
        a , b = self.viewRange()[0]
        if xPixel < minx:
            xPixel = minx
        if xPixel > maxx:
            xPixel = maxx
        return a + int(round((xPixel - minx) * len(self.parent().freqs) * 1. / (maxx - minx), 0)) - 1

    def fromCanvasToClient(self, xPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        inside = True
        vb = self.getPlotItem().getViewBox()
        minx = vb.x()
        maxx = vb.width() + minx
        a , b = self.viewRange()[0]
        if xPixel < minx:
            xPixel = minx
            inside = False
        if xPixel > maxx:
            xPixel = maxx
            inside = False
        return (a + int(round((xPixel - minx) * ( b - a ) * 1. / (maxx - minx), 0)) - 1,inside)

    def fromCanvasToClientY(self, yPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        inside = True
        vb = self.getPlotItem().getViewBox()
        miny = vb.y()
        maxy = vb.height() + miny
        a, b = self.getPlotItem().viewRange()[1]
        yPixel = maxy - yPixel
        if yPixel < miny:
            inside = False
            yPixel = miny
        if yPixel > maxy:
            inside = False
            yPixel = maxy
        return (a + int(round((yPixel - miny) * (b - a) * 1. / (maxy - miny), 0)), inside)

    def getFrequencyAmplitudeInfo(self,x):
        index = numpy.searchsorted(self.parent().freqs,x)
        freq = self.parent().freqs[index]
        amplt = 10*numpy.log10(self.parent().Pxx[index]/numpy.amax(self.parent().Pxx))
        return [freq, amplt]

