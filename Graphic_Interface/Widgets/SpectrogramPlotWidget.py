# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, pyqtSignal
from PyQt4.QtGui import QCursor
from pyqtgraph import GraphicsView
from pyqtgraph.graphicsItems.ImageItem import ImageItem
from pyqtgraph.graphicsItems.ViewBox import ViewBox
import numpy
import  pyqtgraph as pg
from Graphic_Interface.Widgets.Axis import SpecYAxis
from Graphic_Interface.Widgets.Tools import Tools
from Graphic_Interface.Widgets.Tools import RectROI


class SpectrogramPlotWidget(GraphicsView):
    def __init__(self, *args, **kwargs):
        GraphicsView.__init__(self, *args, **kwargs)
        l = QtGui.QGraphicsGridLayout()
        l.setHorizontalSpacing(0)
        l.setVerticalSpacing(0)
        l.setContentsMargins(0, 0, 0, 0)
        self.viewBox = ViewBox()
        self.imageItem = ImageItem()
        self.viewBox.addItem(self.imageItem)
        l.addItem(self.viewBox, 0, 1)
        self.centralWidget.setLayout(l)
        self.xAxis = pg.AxisItem(orientation = 'bottom',linkView=self.parent().axesOscilogram.getPlotItem().getViewBox())
        self.xAxis.setGrid(88)
        l.addItem(self.xAxis, 1, 1)
        self.yAxis = SpecYAxis(self,orientation='left', linkView=self.viewBox)
        self.yAxis.setGrid(88)
        l.addItem(self.yAxis, 0, 0)
        self.xAxis.mouseDragEvent = lambda a : False
        self.yAxis.mouseDragEvent = lambda a : False
        self.viewBox.setMouseEnabled(x=False, y=False)
        self.viewBox.setMenuEnabled(False)
        self.viewBox.setAspectLocked(False)
        self.emitIntervalSpecChanged = True
        #zoomCursor-------------------------------------
        self.zoomRegion = pg.LinearRegionItem([0, 0])
        self.makeZoom = None
        self.makeZoomRect = None
        self.mousePressed = False
        self.mouseZoomEnabled = True

        self.spec_gridx = True
        self.spec_gridy = True
        self.spec_background = "000"


        self.viewBox.addItem(self.zoomRegion)
        self.zoomRegion.sigRegionChanged.connect(self.on_zoomRegionChanged)
        #pointerCursor-----------------------------------
        self.pointerCursor = pg.ScatterPlotItem()
        self.mouseReleased = False
        self.last = {}
        #RectangularCursor-------------------------------
        self.rectangularCursor = RectROI([0, 0], [0, 0], pen=(0,9), movable=False)
        self.rectRegion = {'x':[0,0],'y':[0,0]}
        #------------------------------------------------


        self.setDragMode(QtGui.QGraphicsView.NoDrag)
        self.selectedTool = Tools.Zoom


    PIXELS_OF_CURSORS_CHANGES = 5
    IntervalSpecChanged = pyqtSignal(int, int)
    PointerSpecChanged = pyqtSignal(str)
    PointerCursorPressed = pyqtSignal()
    RectangularCursorPressed = pyqtSignal()
    applyFilter = pyqtSignal(int, int, int, int)

    def load_Theme(self, theme):
        update_graph =False
        self.setBackground(theme.spec_background)
        self.showGrid(theme.spec_GridX,theme.spec_GridY)

        if self.parent() and 'freqs' in self.parent().specgramSettings.__dict__:
            if theme.maxYSpec == -1:
                theme.maxYSpec = self.parent().specgramSettings.freqs[-1]
            YSpec = numpy.searchsorted(self.parent().specgramSettings.freqs, [theme.minYSpec * 1000, theme.maxYSpec * 1000])
            self.viewBox.setRange(yRange=(YSpec[0], YSpec[1]),
                              padding=0, update=True)
            self.parent().refresh(False,True,False)
        if update_graph:
            self.update()


    def clearRectangularCursor(self):
        self.rectRegion['x'] = [0,0]
        self.rectRegion['y'] = [0,0]
        self.rectangularCursor.setPos([0,0])
        self.rectangularCursor.setSize([0,0])

    def clearPointerCursor(self):
        self.pointerCursor.clear()
        self.mouseReleased = False

    def changeSelectedTool(self,tool):
        if tool != self.selectedTool:
            self.selectedTool = tool
            if tool == Tools.PointerCursor:
                self.viewBox.removeItem(self.zoomRegion)
                #self.viewBox.removeItem(self.rectangularCursor)
                self.pointerCursor.clear()
                self.viewBox.addItem(self.pointerCursor)
                self.mouseZoomEnabled = False
                self.mouseReleased = False
                self.rectangularCursor.setPos([0,0])
                self.rectangularCursor.setSize([0,0])
            elif tool == Tools.Zoom:
                self.viewBox.removeItem(self.pointerCursor)
                #self.viewBox.removeItem(self.rectangularCursor)
                self.viewBox.addItem(self.zoomRegion)
                self.zoomRegion.setRegion([0,0])
                self.mouseZoomEnabled = True
                self.emitIntervalSpecChanged = True
                self.rectangularCursor.setPos([0,0])
                self.rectangularCursor.setSize([0,0])
                self.mousePressed = False
            elif tool == Tools.RectangularCursor:
                self.viewBox.removeItem(self.pointerCursor)
                self.viewBox.removeItem(self.zoomRegion)
                self.viewBox.addItem(self.rectangularCursor)
                self.mousePressed = False
            elif tool == Tools.RectangularEraser:
                self.viewBox.removeItem(self.pointerCursor)
                self.viewBox.removeItem(self.zoomRegion)
                self.viewBox.addItem(self.rectangularCursor)
                self.mousePressed = False
            self.update()

    def showGrid(self,x=True,y=True):
        if x:
            self.xAxis.setGrid(88)
        else:
            self.xAxis.setGrid(0)
        if y:
            self.yAxis.setGrid(88)
        else:
            self.yAxis.setGrid(0)

    def on_zoomRegionChanged(self):
        if self.emitIntervalSpecChanged:
            rgn = self.zoomRegion.getRegion()
            self.IntervalSpecChanged.emit(*rgn)

    def mouseMoveEvent(self, event):

        if self.selectedTool == Tools.PointerCursor:
            x = self.fromCanvasToClient(event.x())
            y = self.fromCanvasToClientY(event.y())
            if x == -1 or y == -1:
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                return
            info = self.getFreqTimeAndIntensity(x,y)

            if self.mouseReleased:
                info0 = self.getFreqTimeAndIntensity(self.last['pos'][0],self.last['pos'][1])
                self.PointerSpecChanged.emit(str.format('t0: {0}s  t1 {1}  dt: {2}s',info0[0],info[0],info[0] - info0[0] ))
            else:
                self.PointerSpecChanged.emit(str.format('Time: {0}s          Freq: {1}kHz          Amp: {2}dB',info[0],info[1],info[2]))
            self.viewBox.update()
            self.setCursor(QCursor(QtCore.Qt.CrossCursor))
        elif self.selectedTool == Tools.Zoom:
            #pg.GraphicsView.mouseMoveEvent(self, event)
            pg.GraphicsView.mouseMoveEvent(self, event)
            if self.parent().visibleSpectrogram:
                rgn = self.zoomRegion.getRegion()
                minx, maxx = self.fromClientToCanvas(rgn[0]), self.fromClientToCanvas(rgn[1])
                if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or \
                   abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
                    self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
                elif self.mouseInsideZoomArea(event.x()):
                    if self.mousePressed:
                        self.setCursor(QCursor(QtCore.Qt.ClosedHandCursor))
                    else:
                        self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
                else:
                    self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
        elif self.selectedTool == Tools.RectangularCursor or self.selectedTool == Tools.RectangularEraser:
            x = self.fromCanvasToClient(event.x())
            y = self.fromCanvasToClientY(event.y())

            if self.mousePressed:
                self.RectangularCursorPressed.emit()
                if x < self.last['pos'][0]:
                    if y < self.last['pos'][1]:
                        self.rectangularCursor.setPos([x,y])
                        self.rectRegion['x'][0] = x
                        self.rectRegion['y'][0] = y
                    else:
                        self.rectangularCursor.setPos([x,self.last['pos'][1]])
                        self.rectRegion['x'][0] = x
                        self.rectRegion['y'][0] = self.last['pos'][1]
                elif x >= self.last['pos'][0]:
                    if y < self.last['pos'][1]:
                        self.rectangularCursor.setPos([self.last['pos'][0],y])
                        self.rectRegion['x'][0] = self.last['pos'][0]
                        self.rectRegion['y'][0] = y
                    else:
                        self.rectangularCursor.setPos(self.last['pos'])
                        self.rectRegion['x'][0] = self.last['pos'][0]
                        self.rectRegion['y'][0] = self.last['pos'][1]
                dx = numpy.abs(self.last['pos'][0] - x)
                dy = numpy.abs(self.last['pos'][1] - y)
                self.rectangularCursor.setSize([ dx, dy])
                self.rectRegion['x'][1] = self.rectRegion['x'][0] + dx
                self.rectRegion['y'][1] = self.rectRegion['y'][0] + dy
                info = self.getFreqTimeAndIntensity(self.rectRegion['x'][0], self.rectRegion['y'][0])
                info1 = self.getFreqTimeAndIntensity(self.rectRegion['x'][1], self.rectRegion['y'][1])
                self.rectRegion['y'][0] = info[1]
                self.rectRegion['y'][1] = info1[1]
                self.PointerSpecChanged.emit(str.format('t0: {0}s  t1: {1}s dt: {2}s          MinF: {3}kHz  MaxF: {4}kHz  dF: {5}kHz',info[0],info1[0],info1[0] - info[0],info[1],info1[1],info1[1]-info[1]))
            else:
                info = self.getFreqTimeAndIntensity(x, y)
                if x == -1 or y == -1:
                    self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                    return
                else:
                    self.PointerSpecChanged.emit(str.format("Time: {0}s          Freq: {1}kHz          Amp: {2}dB",info[0],info[1],info[2]))
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
            self.update()

    def mousePressEvent(self, event):
        self.mousePressed = True
        if self.selectedTool == Tools.PointerCursor:
            self.pointerCursor.clear()
            x = self.fromCanvasToClient(event.x())
            y = self.fromCanvasToClientY(event.y())
            if x == -1 or y == -1:
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                return
            self.last = {'pos':[x,y], 'pen': {'color': 'w', 'width': 2},'brush':pg.intColor(255, 255), 'symbol':'+', 'size':20}
            self.pointerCursor.addPoints([self.last])
            self.mouseReleased = False
            self.PointerCursorPressed.emit()
        elif self.selectedTool == Tools.Zoom:
            if not self.zoomRegion in self.items():
                self.zoomRegion.setRegion([self.fromCanvasToClient(event.x()),self.fromCanvasToClient(event.x())])
                self.setZoomRegionVisible(True)
                #self.update()
            else:
                rgn = self.zoomRegion.getRegion()
                minx, maxx = self.fromClientToCanvas(rgn[0]),self.fromClientToCanvas(rgn[1])
                if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or \
                   abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
                    self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
                elif not self.mouseInsideZoomArea(event.x()):
                    x = self.fromCanvasToClient(event.x())
                    self.zoomRegion.setRegion([x, x])
                    #self.update()
                else:
                    self.setCursor(QCursor(QtCore.Qt.ClosedHandCursor))
            pg.GraphicsView.mousePressEvent(self,event)
        elif self.selectedTool == Tools.RectangularCursor or self.selectedTool == Tools.RectangularEraser:
            self.last = {'pos':[self.fromCanvasToClient(event.x()),self.fromCanvasToClientY(event.y())]}
            self.rectangularCursor.setPos(self.last['pos'])
            self.rectangularCursor.setSize([0,0])

    def mouseDoubleClickEvent(self, event):
        if self.selectedTool ==  Tools.Zoom:
            pg.GraphicsView.mouseDoubleClickEvent(self, event)
            if self.mouseInsideZoomArea(event.x()) and self.makeZoom and callable(self.makeZoom):
                rgn = self.zoomRegion.getRegion()
                if rgn[0] == rgn[1]:
                    return
                self.makeZoom(rgn[0], rgn[1], specCoords=True)
               
        elif self.selectedTool ==  Tools.RectangularCursor:
            x = self.fromCanvasToClient(event.x())
            y = numpy.round(self.parent().specgramSettings.freqs[self.fromCanvasToClientY(event.y())]*1.0/1000,1)
            if self.mouseInsideRectArea(x,y):
                self.makeZoomRect(specCoords = True)
        elif self.selectedTool == Tools.RectangularEraser:
             x = self.fromCanvasToClient(event.x())
             y = numpy.round(self.parent().specgramSettings.freqs[self.fromCanvasToClientY(event.y())]*1.0/1000,1)
             if self.mouseInsideRectArea(x,y):
                self.applyFilter.emit(self.rectRegion['x'][0],self.rectRegion['x'][1],self.rectRegion['y'][0]*1000,self.rectRegion['y'][1]*1000)

    def mouseReleaseEvent(self, event):
        self.mousePressed = False
        if self.selectedTool == Tools.PointerCursor or self.selectedTool == Tools.RectangularCursor:
            self.mouseReleased = True
            #pg.GraphicsView.mouseReleaseEvent(self, event)
        elif self.selectedTool == Tools.Zoom:
            pg.GraphicsView.mouseReleaseEvent(self, event)
            rgn = self.zoomRegion.getRegion()
            minx, maxx = self.fromClientToCanvas(rgn[0]), self.fromClientToCanvas(rgn[1])
            if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or \
               abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
                self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
            elif self.mouseInsideZoomArea(event.x()):
                self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
            else:
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

            self.parent().emit(SIGNAL("IntervalChanged"))

    def mouseInsideRectArea(self,x,y):
        return x <= self.rectRegion['x'][1] and x >= self.rectRegion['x'][0]\
               and y <= self.rectRegion['y'][1] and y >= self.rectRegion['y'][0]

    def mouseInsideZoomArea(self, xPixel):
        xIndex = self.fromCanvasToClient(xPixel)
        rgn = self.zoomRegion.getRegion()
        return rgn[0] <= xIndex <= rgn[1]

    def fromClientToCanvas(self, indexX):
        """
        Translates the index in the signal array to its corresponding coordinates in the canvas
        """
        maxx = self.viewBox.width()
        a, b = self.viewBox.viewRange()[0]
        return int(self.viewBox.x() + round((maxx) * (indexX - a) * 1. / (b - a), 0))

    def fromCanvasToClient(self, xPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        minx = self.viewBox.x()
        maxx = self.viewBox.width() + minx
        a, b = self.imageItem.getViewBox().viewRange()[0]
        if xPixel < minx:
            if self.selectedTool == Tools.PointerCursor:
                self.pointerCursor.clear()
                if self.mouseReleased:
                    self.pointerCursor.addPoints([self.last])
                return -1
            elif self.selectedTool == Tools.RectangularCursor  or self.selectedTool == Tools.RectangularEraser:
                xPixel = minx
        if xPixel > maxx:
            if self.selectedTool == Tools.PointerCursor:
                self.pointerCursor.clear()
                if self.mouseReleased:
                    self.pointerCursor.addPoints([self.last])
                return -1
            elif self.selectedTool == Tools.RectangularCursor  or self.selectedTool == Tools.RectangularEraser:
                xPixel = maxx
        return a + int(round((xPixel - minx) * (b - a) * 1. / (maxx - minx), 0))

    def fromCanvasToClientY(self, yPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        miny = self.viewBox.y()
        maxy = self.viewBox.height() + miny
        a, b = self.imageItem.getViewBox().viewRange()[1]
        yPixel = maxy - yPixel
        if yPixel < miny:
            if self.selectedTool == Tools.RectangularCursor or self.selectedTool == Tools.RectangularEraser:
                yPixel = miny
            else:
                self.pointerCursor.clear()
                if self.mouseReleased:
                    self.pointerCursor.addPoints([self.last])
                return -1
        if yPixel > maxy:
            if self.selectedTool == Tools.RectangularCursor  or self.selectedTool == Tools.RectangularEraser:
                yPixel = maxy
            else:
                self.pointerCursor.clear()
                if self.mouseReleased:
                    self.pointerCursor.addPoints([self.last])
                return -1

        return a + int(round((yPixel - miny) * (b - a) * 1. / (maxy - miny), 0))

    def getFreqTimeAndIntensity(self,x,y):
        #YSpec = numpy.searchsorted(self.parent().specgramSettings.freqs, self.parent().minYSpc*1000)
        time = numpy.round((self.parent().mainCursor.min + self.parent()._from_spec_to_osc(x))*1.0/self.parent().signalProcessor.signal.samplingRate,2)
        freq = numpy.round(self.parent().specgramSettings.freqs[y]*1.0/1000,1)
        intensity = numpy.round(10*numpy.log10(self.parent().specgramSettings.Pxx[y][x - self.parent()._from_osc_to_spec(self.parent().mainCursor.min)-1]*1.0/numpy.amax(self.parent().specgramSettings.Pxx)),2)
        return [time, freq, intensity]