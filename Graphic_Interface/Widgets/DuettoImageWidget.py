from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, pyqtSignal
from PyQt4.QtGui import QCursor
from pyqtgraph import GraphicsView
from pyqtgraph.graphicsItems.AxisItem import AxisItem
from pyqtgraph.graphicsItems.ImageItem import ImageItem
from pyqtgraph.graphicsItems.ViewBox import ViewBox
import numpy
import  pyqtgraph as pg
from Graphic_Interface.Widgets.Tools import Tools

class SpecYAxis(pg.AxisItem):
    def __init__(self,*args,**kwargs):
        pg.AxisItem.__init__(self,*args,**kwargs)
        self.freqs = None
        self.setLabel(text="Frequency (KHz)")
    def tickStrings(self, values, scale, spacing):
        if self.freqs is None:
            return values
        r = self.freqs[[x for x in values if x < len(self.freqs)]]
        for i in range(len(r)):
            r[i] = "{:.1f}".format(r[i]/1000.0)
        return r
    def refresh(self,freqs):
        self.freqs = freqs



class DuettoImageWidget(GraphicsView):
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
        self.yAxis = SpecYAxis(orientation='left', linkView=self.viewBox)
        self.yAxis.setGrid(88)
        l.addItem(self.yAxis, 0, 0)
        self.viewBox.setMouseEnabled(x=False, y=False)
        self.viewBox.setAspectLocked(False)
        self.emitIntervalSpecChanged = True
        self.zoomRegion = pg.LinearRegionItem([0, 0])

        #pointerCursor-----------------------------------
        self.pointerCursor = pg.ScatterPlotItem()
        self.setDragMode(QtGui.QGraphicsView.NoDrag)
        self.selectedTool = Tools.Zoom
        self.mouseReleased = False
        self.last = {}
        self.zoomRegion.sigRegionChanged.connect(self.on_zoomRegionChanged)
        self.viewBox.addItem(self.zoomRegion)
        self.makeZoom = None
        self.mousePressed = False
        self.mouseZoomEnabled = True

    PIXELS_OF_CURSORS_CHANGES = 5
    IntervalSpecChanged = pyqtSignal(int, int)
    PointerSpecChanged = pyqtSignal(str)
    PointerCursorPressed = pyqtSignal()

    def clearPointerCursor(self):
        self.pointerCursor.clear()
        self.mouseReleased = False

    def changeSelectedTool(self,tool):
        if tool != self.selectedTool:
            self.selectedTool = tool
            if tool == Tools.PointerCursor:
                self.viewBox.removeItem(self.zoomRegion)
                self.pointerCursor.clear()
                self.viewBox.addItem(self.pointerCursor)
                self.mouseZoomEnabled = False
                self.mouseReleased = False
            elif tool == Tools.Zoom:
                self.viewBox.removeItem(self.pointerCursor)
                self.viewBox.addItem(self.zoomRegion)
                self.zoomRegion.setRegion([0,0])
                self.mouseZoomEnabled = True
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
            pg.GraphicsView.mouseMoveEvent(self, event)

            x = self.fromCanvasToClient(event.x())
            y = self.fromCanvasToClientY(event.y())
            if x == -1 or y == -1:
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                return
            info = self.getFreqTimeAndIntensity(x,y)

            if self.mouseReleased:
                info0 = self.getFreqTimeAndIntensity(self.last['pos'][0],self.last['pos'][1])
                self.PointerSpecChanged.emit(str.format('t0: {0}s  dt: {1}s  Intensity: {2}dB',info0[0],info[0] - info0[0] ,info[2]))
            else:
                self.PointerSpecChanged.emit(str.format('Time: {0}s  Frequency: {1}kHz Intensity: {2}dB',info[0],info[1],info[2]))
            self.viewBox.update()
            self.setCursor(QCursor(QtCore.Qt.CrossCursor))
        elif self.selectedTool == Tools.Zoom:
            pg.GraphicsView.mouseMoveEvent(self, event)
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

    def mousePressEvent(self, event):
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
        if self.selectedTool == Tools.Zoom:
            self.mousePressed = True
            if not self.zoomRegion in self.items():
                self.zoomRegion.setRegion([self.fromCanvasToClient(event.x()),self.fromCanvasToClient(event.x())])
                #self.setZoomRegionVisible(True)
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

    def mouseDoubleClickEvent(self, event):
        if self.selectedTool ==  Tools.Zoom:
            pg.GraphicsView.mouseDoubleClickEvent(self, event)
            if self.mouseInsideZoomArea(event.x()) and self.makeZoom and callable(self.makeZoom):
                rgn = self.zoomRegion.getRegion()
                if rgn[0] == rgn[1]:
                    return
                self.makeZoom(rgn[0], rgn[1], specCoords=True)
                self.zoomRegion.setRegion([rgn[0], rgn[0]])
                #self.zoomRegion.lineMoved()

    def mouseReleaseEvent(self, event):
        if self.selectedTool == Tools.PointerCursor:
            self.mouseReleased = True
            #pg.GraphicsView.mouseReleaseEvent(self, event)
        elif self.selectedTool == Tools.Zoom:
            self.mousePressed = False
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

    #PIXELS_BETWEEN_AXES_AND_DATA = 9 #the pixels for the numbers in the left side

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
        if xPixel > maxx:
            if self.selectedTool == Tools.PointerCursor:
                self.pointerCursor.clear()
                if self.mouseReleased:
                    self.pointerCursor.addPoints([self.last])
                return -1
        return a + int(round((xPixel - minx) * (b - a) * 1. / (maxx - minx), 0))

    def fromCanvasToClientY(self, yPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        miny = self.viewBox.y()
        maxy = self.viewBox.height() + miny
        a, b = self.imageItem.getViewBox().viewRange()[1]
        yPixel = maxy - yPixel
        if yPixel < miny or yPixel > maxy:
            self.pointerCursor.clear()
            if self.mouseReleased:
                self.pointerCursor.addPoints([self.last])
            return -1

        return a + int(round((yPixel - miny) * (b - a) * 1. / (maxy - miny), 0))

    def getFreqTimeAndIntensity(self,x,y):
        time =  self.parent()._from_spec_to_osc(x)*1.0/self.parent().signalProcessor.signal.samplingRate
        freq = numpy.round(self.parent().specgramSettings.freqs[y]*1.0/1000,1)
        intensity = 10*numpy.log10(self.parent().specgramSettings.Pxx[y][x - self.parent()._from_osc_to_spec(self.parent().mainCursor.min)]*1.0/numpy.amax(self.parent().specgramSettings.Pxx))
        return [time, freq, intensity]