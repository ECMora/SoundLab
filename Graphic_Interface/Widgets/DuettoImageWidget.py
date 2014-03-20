from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, pyqtSignal
from PyQt4.QtGui import QCursor
from pyqtgraph import GraphicsView
from pyqtgraph.graphicsItems.AxisItem import AxisItem
from pyqtgraph.graphicsItems.ImageItem import ImageItem
from pyqtgraph.graphicsItems.ViewBox import ViewBox
import  pyqtgraph as pg

class SpecXAxis(pg.AxisItem):
    def __init__(self,*args,**kwargs):
        pg.AxisItem.__init__(self,*args,**kwargs)
        self.bins = None
    def tickStrings(self, values, scale, spacing):
        self.setLabel(text="Time (s)")
        if self.bins is None:
            return values
        return self.bins[values]
    def refresh(self,bins):
        self.bins = bins

class SpecYAxis(pg.AxisItem):
    def __init__(self,*args,**kwargs):
        pg.AxisItem.__init__(self,*args,**kwargs)
        self.freqs = None
    def tickStrings(self, values, scale, spacing):
        #self.setLabel(text="KHz")
        if self.freqs is None:
            return values
        r  = self.freqs[values]
        for i in range(len(r)):
            r[i] = (int((r[i]/100)))/10.0
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
        self.xAxis = SpecXAxis(orientation = 'bottom',linkView=self.viewBox)
        l.addItem(self.xAxis, 1, 1)
        self.yAxis = SpecYAxis(orientation='left', linkView=self.viewBox)
        l.addItem(self.yAxis, 0, 0)
        self.viewBox.setMouseEnabled(x=False, y=False)
        self.viewBox.setAspectLocked(False)
        self.zoomRegion= pg.LinearRegionItem([0,0])
        self.viewBox.addItem(self.zoomRegion)
        self.makeZoom = None
        self.mousePressed = False
        #self.viewBox.setRange(xRange=(0, 10), padding=0)

    PIXELS_OF_CURSORS_CHANGES = 5
    IntervalSpecChanged = pyqtSignal(int, int)

    def mouseMoveEvent(self, event):
       pg.ImageView.mouseMoveEvent(self,event)
       if self.parent().visibleOscilogram:
           if self.mousePressed and not self.mouseInsideZoomArea(event.x()):

               now = self.fromCanvasToClient(event.x())
               if self.fromCanvasToClient(self.lastX) > now:
                    self.zoomRegion.setRegion([now,self.fromCanvasToClient(self.lastX)])
                    self.IntervalSpecChanged.emit(now,self.fromCanvasToClient(self.lastX))
               else:
                   self.zoomRegion.setRegion([self.fromCanvasToClient(self.lastX),now])
                   self.IntervalSpecChanged.emit(self.fromCanvasToClient(self.lastX),now)
               self.zoomRegion.lineMoved()
           if not self.mousePressed and self.mouseInsideZoomArea(event.x()):
               rgn = self.zoomRegion.getRegion()
               self.IntervalSpecChanged.emit(rgn[0],rgn[1])
               self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
           elif not self.mouseInsideZoomArea(event.x()):
               self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
           rgn = self.zoomRegion.getRegion()
           minx, maxx = self.fromClientToCanvas(rgn[0]),self.fromClientToCanvas(rgn[1])
           if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES or abs(
                           maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
               self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))

    def mousePressEvent(self, event):
         if(not self.zoomRegion in self.items()):
             self.zoomRegion.setRegion([self.fromCanvasToClient(event.x()),self.fromCanvasToClient(event.x())])
             self.IntervalSpecChanged.emit(self.fromCanvasToClient(event.x()),self.fromCanvasToClient(event.x()))
             self.update()
         elif not self.mouseInsideZoomArea(event.x()):
             self.zoomRegion.setRegion([self.fromCanvasToClient(event.x()),self.fromCanvasToClient(event.x())])
             self.IntervalSpecChanged.emit(self.fromCanvasToClient(event.x()),self.fromCanvasToClient(event.x()))
             #self.setZoomRegionVisible(True)
             self.update()
         pg.GraphicsView.mousePressEvent(self,event)
         self.mousePressed = True
         if self.mouseInsideZoomArea(event.x()):
             self.setCursor(QCursor(QtCore.Qt.ClosedHandCursor))
         self.lastX = event.x()
         rgn = self.zoomRegion.getRegion()
         minx, maxx = self.fromClientToCanvas(rgn[0]),self.fromClientToCanvas(rgn[1])
         if abs(minx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
             self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
             self.lastX = maxx
         if abs(maxx - event.x()) < self.PIXELS_OF_CURSORS_CHANGES:
             self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
             self.lastX = minx

    def mouseDoubleClickEvent(self, event):
        pg.ImageView.mouseDoubleClickEvent(self,event)
        if self.mouseInsideZoomArea(event.x()) and self.makeZoom is not None and callable(self.makeZoom):
            rgn = self.zoomRegion.getRegion()
            self.makeZoom(rgn[0],rgn[1])
            self.zoomRegion.setRegion([rgn[0],rgn[0]])
            self.IntervalSpecChanged.emit(rgn[0],rgn[0])
            self.zoomRegion.lineMoved()

    def mouseReleaseEvent(self, event):
        pg.GraphicsView.mouseReleaseEvent(self,event)
        self.lastX = event.x()

        if self.mouseInsideZoomArea(event.x()):
            self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
        else:
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
        self.mousePressed = False
        self.parent().emit(SIGNAL("IntervalChanged"))

    def mouseInsideZoomArea(self, xPixel):
        xIndex = self.fromCanvasToClient(xPixel)
        rgn = self.zoomRegion.getRegion()
        return xIndex >= rgn[0] and xIndex <= rgn[1]

    def fromClientToCanvas(self, indexX):
       """
       Translates the index in the signal array to its corresponding coordinates in the canvas
       """
       maxx = self.width()
       a, b = self.imageItem.getViewBox().viewRange()[0]
       return int(self.PIXELS_BETWEEN_AXES_AND_DATA + round((maxx) * (indexX - a) * 1. / (b - a),0))

    PIXELS_BETWEEN_AXES_AND_DATA = 9 #the pixels for the numbers in the left side

    def fromCanvasToClient(self, xPixel):
        """
        Translates the coordinates from the canvas to its corresponding  index in the signal array
        """
        minx, maxx = 0, self.width()
        a, b = self.imageItem.getViewBox().viewRange()[0]
        if xPixel < minx:
            xPixel = minx
        if xPixel > maxx:
            xPixel = maxx
        return a + int(round((xPixel-self.PIXELS_BETWEEN_AXES_AND_DATA) * (b - a) * 1. / (maxx - minx),0))
