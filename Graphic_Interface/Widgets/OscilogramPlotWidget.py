# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, pyqtSignal, QRect
from PyQt4.QtGui import QCursor,QColor
import pyqtgraph as pg
import numpy
from Graphic_Interface.Widgets.Tools import Tools
from Graphic_Interface.Widgets.Tools import RectROI

class OscilogramPlotWidget(pg.PlotWidget):
    def __init__(self,  parent=None,**kargs):
        pg.PlotWidget.__init__(self, **kargs)
        self.mousePressed = False
        self.emitIntervalOscChanged = True
        self.osc_background = "000"
        self.osc_gridx = True
        self.osc_gridy = True
        self.getPlotItem().showGrid(x=self.osc_gridx, y=self.osc_gridy)

        self.zoomRegion = pg.LinearRegionItem([0, 0])
        self.zoomRegion.sigRegionChanged.connect(self.on_zoomRegionChanged)
        self.makeZoom = None
        self.makeZoomRect = None
        self.setZoomRegionVisible(True)
        self.getPlotItem().setMouseEnabled(x=False, y=False)

        self.setClipToView(True)
        self.setDownsampling(auto=True, mode="peak")
        self.setMouseEnabled(x=False, y=False)
        self.setMenuEnabled(False)
        self.getPlotItem().hideButtons()
        self.setRange(QRect(0, 0, 1, 1))

        self.threshold = pg.InfiniteLine(movable=True, angle=0, pos=0)

        self.decimalPlaces = 5

        self.highligthedElement =  pg.LinearRegionItem([0, 0],movable=False, brush=pg.mkBrush(QColor(255,255,255)))
        self.getPlotItem().getViewBox().addItem(self.highligthedElement)

        self.mouseZoomEnabled = True
        self.currentTextInfo = pg.TextItem("Duetto",color=(255,255,255),anchor=(0.5,0.5))#the label with the current information of the mouse int the widget's s
         #pointerCursor-----------------------------------
        self.pointerCursor = pg.ScatterPlotItem()
        self.isSelectedRect = False
        self.rectangularCursor = RectROI([0, 0], [0, 0], pen=(0,9), movable=False)
        self.rectRegion = {'x':[0,0],'y':[0,0]}
        self.selectedTool = Tools.Zoom
        self.mouseReleased = False
        self.last = {}
        self.show()

    def load_Theme(self, theme):
        update_graph =False
        if self.osc_background != theme.osc_background:
            self.osc_background = theme.osc_background
            self.setBackground(self.osc_background)

        if self.osc_gridx != theme.osc_GridX or self.osc_gridy != theme.osc_GridY:
            self.osc_gridx = theme.osc_GridX
            self.osc_gridy = theme.osc_GridY
            self.getPlotItem().showGrid(x=self.osc_gridx, y=self.osc_gridy)


        if update_graph:
            self.update()


    def select_region(self,indexFrom,indexTo,brush=None):
        """
        Highlight a section in the graph.
        @param indexFrom: The start of the selected  section
        @param indexTo: The end of the selected  section
        @param brush: optional brush to paint inside the section
        """
        self.highligthedElement.setRegion([indexFrom,indexTo])
        self.highligthedElement.setBrush(brush if brush is not None else pg.mkBrush(QColor(255,255,255)))
        self.update(indexFrom,-2**16,indexTo,2**16)

    def on_zoomRegionChanged(self):
        if self.emitIntervalOscChanged:
            rgn = self.zoomRegion.getRegion()
            self.IntervalOscChanged.emit(*rgn)

    def setVisibleThreshold(self,bool):
        if bool and self.threshold not in self.getPlotItem().getViewBox().addedItems:
            self.getPlotItem().getViewBox().addItem(self.threshold)
        elif not bool and self.threshold in self.getPlotItem().getViewBox().addedItems:
            self.getPlotItem().getViewBox().removeItem(self.threshold)

    PointerOscChanged = pyqtSignal(str)
    IntervalOscChanged = pyqtSignal(int, int)
    PointerCursorPressed = pyqtSignal()
    RectangularCursorPressed = pyqtSignal()
    PIXELS_OF_CURSORS_CHANGES = 5

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
                self.setZoomRegionVisible(value = False)
                #self.removeItem(self.rectangularCursor)
                self.pointerCursor.clear()
                self.addItem(self.pointerCursor)
                self.mouseZoomEnabled = False
                self.mouseReleased = False
                self.rectangularCursor.setPos([0,0])
                self.rectangularCursor.setSize([0,0])
            elif tool == Tools.Zoom:
                self.removeItem(self.pointerCursor)
                #self.removeItem(self.rectangularCursor)
                self.setZoomRegionVisible(value = True)
                self.zoomRegion.setRegion([0,0])
                self.mouseZoomEnabled = True
                self.mousePressed = False
                self.rectangularCursor.setPos([0,0])
                self.rectangularCursor.setSize([0,0])
            elif tool == Tools.RectangularCursor:
                self.removeItem(self.pointerCursor)
                self.setZoomRegionVisible(value = False)
                self.addItem(self.rectangularCursor)
                self.mousePressed = False
            elif tool == Tools.RectangularEraser:
                self.removeItem(self.pointerCursor)
                self.setZoomRegionVisible(value = False)
            self.update()

    def setZoomRegionVisible(self, value=False):
        if value and self.zoomRegion not in self.items():
            self.addItem(self.zoomRegion)
        elif not value and self.zoomRegion in self.items():
            self.removeItem(self.zoomRegion)
        #self.update()

    def mouseMoveEvent(self, event):

        if self.selectedTool == Tools.PointerCursor:
            if self.mousePressed:return

            x = self.fromCanvasToClient(event.x())
            y = self.fromCanvasToClientY(event.y())
            info = self.getAmplitudeTimeInfo(x,y)
            info = round(info[0],self.decimalPlaces),round(info[1],self.decimalPlaces)
            if x == -1 or y == -1:
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                return
            if self.mouseReleased:
                 info0 = self.getAmplitudeTimeInfo(self.last['pos'][0],self.last['pos'][1])
                 info0 = round(info0[0],self.decimalPlaces),round(info0[1],self.decimalPlaces)

                 self.PointerOscChanged.emit(str.format('t0: {0}s  dt: {1}s  Amplitude: {2}%',info0[0],info[0] - info0[0] ,info[1]))
            else:
                self.PointerOscChanged.emit(str.format('Time: {0}s  Amplitude: {1}%',info[0],info[1]))
            #self.viewBox.update()
            self.setCursor(QCursor(QtCore.Qt.CrossCursor))
        elif self.selectedTool == Tools.Zoom:
            pg.PlotWidget.mouseMoveEvent(self, event)
            if self.parent().visibleOscilogram:
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
        elif self.selectedTool == Tools.RectangularEraser:
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
        elif self.selectedTool == Tools.RectangularCursor:
            if self.rectangularCursor not in self.items():
                self.addItem(self.rectangularCursor)
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
                info = self.getAmplitudeTimeInfo(self.rectRegion['x'][0], self.rectRegion['y'][0])
                info = round(info[0],self.decimalPlaces),round(info[1],self.decimalPlaces)

                info1 = self.getAmplitudeTimeInfo(self.rectRegion['x'][1], self.rectRegion['y'][1])
                info1 = round(info1[0],self.decimalPlaces),round(info1[1],self.decimalPlaces)

                self.rectRegion['y'][0] = info[1]
                self.rectRegion['y'][1] = info1[1]
                self.PointerOscChanged.emit(str.format('t0: {0}s  t1: {1}s dt: {2}s  Max Amplitude: {3}% Min Amplitude: {4}% ',info[0],info1[0],info1[0] - info[0],info[1],info1[1]))
            else:
                info = self.getAmplitudeTimeInfo(x, y)
                info = round(info[0],self.decimalPlaces),round(info[1],self.decimalPlaces)


                if x == -1 or y == -1:
                    self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                    return
                else:
                    self.PointerOscChanged.emit(str.format('Time: {0}s  Amplitude: {1}%',info[0],info[1]))
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
            #pg.PlotWidget.mousePressEvent(self, event)
            #self.update()
            self.PointerCursorPressed.emit()
        elif self.selectedTool == Tools.Zoom:
            if self.zoomRegion not in self.items():
                self.zoomRegion.setRegion([self.fromCanvasToClient(event.x()), self.fromCanvasToClient(event.x())])
                self.setZoomRegionVisible(True)
                #self.update()
            else:
                rgn = self.zoomRegion.getRegion()
                minx, maxx = self.fromClientToCanvas(rgn[0]), self.fromClientToCanvas(rgn[1])
                if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or \
                   abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
                    self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
                elif not self.mouseInsideZoomArea(event.x()):
                    x = self.fromCanvasToClient(event.x())
                    self.zoomRegion.setRegion([x, x])
                    #self.update()
                else:
                    self.setCursor(QCursor(QtCore.Qt.ClosedHandCursor))
            pg.PlotWidget.mousePressEvent(self, event)
        elif self.selectedTool == Tools.RectangularCursor:
            self.last = {'pos':[self.fromCanvasToClient(event.x()),self.fromCanvasToClientY(event.y())]}
            self.rectangularCursor.setPos(self.last['pos'])
            self.rectangularCursor.setSize([0,0])

    def mouseDoubleClickEvent(self, event):
        if self.selectedTool == Tools.Zoom:
            pg.PlotWidget.mouseDoubleClickEvent(self, event)
            if self.mouseInsideZoomArea(event.x()) and self.makeZoom and callable(self.makeZoom):
                rgn = self.zoomRegion.getRegion()
                if rgn[0] == rgn[1]:
                    return
                self.makeZoom(rgn[0], rgn[1])
                self.zoomRegion.setRegion([rgn[0], rgn[0]])
        elif self.selectedTool ==  Tools.RectangularCursor:
            x = self.fromCanvasToClient(event.x())
            y = self.fromCanvasToClientY(event.y())
            y = numpy.round(y*100.0/self.parent().signalProcessor.signal.getMaximumValueAllowed(),0)
            if self.mouseInsideRectArea(x,y):
                self.makeZoomRect()

    def mouseReleaseEvent(self, event):
        self.mousePressed = False
        if self.selectedTool == Tools.PointerCursor or self.selectedTool == Tools.RectangularCursor:
            self.mouseReleased = True

        elif self.selectedTool == Tools.Zoom:

            pg.PlotWidget.mouseReleaseEvent(self, event)

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
        @param indexX:  The signal index
        @return:  the canvas coordinates
        """
        vb = self.getPlotItem().getViewBox()
        maxx = vb.width()
        a, b = self.getPlotItem().viewRange()[0]
        return int(vb.x() + round((maxx) * (indexX - a) * 1. / (b - a), 0))

    def fromCanvasToClient(self, xPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        vb = self.getPlotItem().getViewBox()
        minx = vb.x()
        maxx = vb.width() + minx
        a, b = self.getPlotItem().viewRange()[0]
        if xPixel < minx:
            if self.selectedTool == Tools.PointerCursor:
                self.pointerCursor.clear()
                if self.mouseReleased:
                    self.pointerCursor.addPoints([self.last])
                return -1
            elif self.selectedTool == Tools.RectangularCursor:
                xPixel = minx
        if xPixel > maxx:
            if self.selectedTool == Tools.PointerCursor:
                self.pointerCursor.clear()
                if self.mouseReleased:
                    self.pointerCursor.addPoints([self.last])
                return -1
            elif self.selectedTool == Tools.RectangularCursor:
                xPixel = maxx
        return a + int(round((xPixel - minx) * (b - a) * 1. / (maxx - minx), 0))

    def fromCanvasToClientY(self, yPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        vb = self.getPlotItem().getViewBox()
        miny = vb.y()
        maxy = vb.height() + miny
        a, b = self.getPlotItem().viewRange()[1]
        yPixel = maxy - yPixel
        if yPixel < miny:
            if self.selectedTool == Tools.RectangularCursor:
                yPixel = miny
            else:
                self.pointerCursor.clear()
                if self.mouseReleased:
                    self.pointerCursor.addPoints([self.last])
                return -1
        if yPixel > maxy:
            if self.selectedTool == Tools.RectangularCursor:
                yPixel = maxy
            else:
                self.pointerCursor.clear()
                if self.mouseReleased:
                    self.pointerCursor.addPoints([self.last])
                return -1
        return a + int(round((yPixel - miny) * (b - a) * 1. / (maxy - miny), 0))

    def getAmplitudeTimeInfo(self,x,y):
        amplt = numpy.round(y*100.0/self.parent().signalProcessor.signal.getMaximumValueAllowed(),0)
        time = x*1.0/self.parent().signalProcessor.signal.samplingRate
        return [time, amplt]
