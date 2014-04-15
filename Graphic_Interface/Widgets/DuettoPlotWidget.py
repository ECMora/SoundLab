from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL, pyqtSignal
from PyQt4.QtGui import QCursor
import pyqtgraph as pg
import numpy

class DuettoPlotWidget(pg.PlotWidget):
    def __init__(self,  parent=None,**kargs):
        pg.PlotWidget.__init__(self, **kargs)
        self.mousePressed = False
        self.emitIntervalOscChanged = True
        self.zoomRegion = pg.LinearRegionItem([0, 0])
        self.zoomRegion.sigRegionChanged.connect(self.on_zoomRegionChanged)
        self.makeZoom = None
        self.getPlotItem().setMouseEnabled(x=False, y=False)
        self.threshold = pg.InfiniteLine(movable=True, angle=0, pos=0)
        self.mouseZoomEnabled = True
        self.currentTextInfo = pg.TextItem("oioioioi",color=(255,255,255),anchor=(0.5,0.5))#the label with the current information of the mouse int the widget's s
         #pointerCursor-----------------------------------
        self.pointerCursor = pg.ScatterPlotItem()
        self.selectedTool = 'ZoomCursor'
        self.mouseReleased = False
        self.last = {}

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
    PIXELS_OF_CURSORS_CHANGES = 5

    def resetCursors(self):
        self.pointerCursor.clear()
        self.mouseReleased = False

    def changeSelectedTool(self,tool):
        if tool != self.selectedTool:
            vb = self.getPlotItem().getViewBox()
            self.selectedTool = tool
            if tool == 'PointerCursor':
                self.removeItem(self.zoomRegion)
                self.pointerCursor.clear()
                self.addItem(self.pointerCursor)
                self.mouseZoomEnabled = False
                self.mouseReleased = False
            elif tool == 'ZoomCursor':
                self.removeItem(self.pointerCursor)
                self.addItem(self.zoomRegion)
                self.zoomRegion.setRegion([0,0])
                self.mouseZoomEnabled = True
            self.update()

    def setZoomRegionVisible(self, value=False):
        if value and self.zoomRegion not in self.items():
            self.addItem(self.zoomRegion)
        elif not value and self.zoomRegion in self.items():
            self.removeItem(self.zoomRegion)
        #self.update()

    def mouseMoveEvent(self, event):
        if self.selectedTool == 'PointerCursor':
            pg.PlotWidget.mouseMoveEvent(self, event)

            x = self.fromCanvasToClient(event.x())
            y = self.fromCanvasToClientY(event.y())
            info = self.getAmplitudeTimeInfo(x,y)
            if x == -1 or y == -1:
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                return
            if self.mouseReleased:
                 info0 = self.getAmplitudeTimeInfo(self.last['pos'][0],self.last['pos'][1])
                 self.PointerOscChanged.emit(str.format('t0: {0}s  dt: {1}s  Amplitude: {2}%',info0[0],info[0] - info0[0] ,info[1]))
            else:
                self.PointerOscChanged.emit(str.format('Time: {0}s  Amplitude: {1}%',info[0],info[1]))
            #self.viewBox.update()
            self.setCursor(QCursor(QtCore.Qt.CrossCursor))
        if self.mouseZoomEnabled:
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


    def mousePressEvent(self, event):
        if self.selectedTool == 'PointerCursor':
            self.pointerCursor.clear()
            x = self.fromCanvasToClient(event.x())
            y = self.fromCanvasToClientY(event.y())
            if x == -1 or y == -1:
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                return
            self.last = {'pos':[x,y], 'pen': {'color': 'w', 'width': 2},'brush':pg.intColor(255, 255), 'symbol':'+', 'size':20}
            self.pointerCursor.addPoints([self.last])
            self.mouseReleased = False
            pg.PlotWidget.mousePressEvent(self, event)
        if self.mouseZoomEnabled:
            self.mousePressed = True
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

    def mouseDoubleClickEvent(self, event):
        if self.mouseZoomEnabled:
            pg.PlotWidget.mouseDoubleClickEvent(self, event)
            if self.mouseInsideZoomArea(event.x()) and self.makeZoom and callable(self.makeZoom):
                rgn = self.zoomRegion.getRegion()
                self.makeZoom(rgn[0], rgn[1])
                self.zoomRegion.setRegion([rgn[0], rgn[0]])
                #self.zoomRegion.lineMoved()

    def mouseReleaseEvent(self, event):
        if self.selectedTool == 'PointerCursor':
            self.mouseReleased = True
            pg.PlotWidget.mouseReleaseEvent(self, event)
        if self.mouseZoomEnabled:
            self.mousePressed = False
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


    def mouseInsideZoomArea(self, xPixel):
        xIndex = self.fromCanvasToClient(xPixel)
        rgn = self.zoomRegion.getRegion()
        return rgn[0] <= xIndex <= rgn[1]

    def fromClientToCanvas(self, indexX):
        """
        Translates the index in the signal array to its corresponding coordinates in the canvas
        """
        vb = self.getPlotItem().getViewBox()
        maxx = vb.width()
        a, b = self.getPlotItem().viewRange()[0]
        return int(vb.x() + round((maxx) * (indexX - a) * 1. / (b - a), 0))

    #PIXELS_BETWEEN_AXES_AND_DATA = 10 #the pixels for the numbers in the left side

    def fromCanvasToClient(self, xPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        vb = self.getPlotItem().getViewBox()
        minx = vb.x()
        maxx = vb.width() + minx
        a, b = self.getPlotItem().viewRange()[0]
        if xPixel < minx:
            if self.selectedTool == 'PointerCursor':
                self.pointerCursor.clear()
                if self.mouseReleased:
                    self.pointerCursor.addPoints([self.last])
                return -1
        if xPixel > maxx:
            if self.selectedTool == 'PointerCursor':
                self.pointerCursor.clear()
                if self.mouseReleased:
                    self.pointerCursor.addPoints([self.last])
                return -1
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
        if yPixel < miny or yPixel > maxy:
            self.pointerCursor.clear()
            if self.mouseReleased:
                self.pointerCursor.addPoints([self.last])
            return -1
        return a + int(round((yPixel - miny) * (b - a) * 1. / (maxy - miny), 0))

    def getAmplitudeTimeInfo(self,x,y):
        amplt = numpy.round(y*100.0/self.getPlotItem().axes['left']['item'].Max,0)
        time = x*1.0/self.getPlotItem().axes['bottom']['item'].Fs
        return [time, amplt]
