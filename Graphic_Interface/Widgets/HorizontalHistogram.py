from pyqtgraph.Qt import QtGui
import pyqtgraph.functions as fn
from pyqtgraph.Point import Point
from pyqtgraph.graphicsItems.AxisItem import AxisItem
from pyqtgraph.graphicsItems.HistogramLUTItem import HistogramLUTItem
from pyqtgraph.graphicsItems.LinearRegionItem import LinearRegionItem
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from pyqtgraph.widgets.HistogramLUTWidget import HistogramLUTWidget


class HorizontalHistogramWidget(HistogramLUTWidget):
    def __init__(self, parent=None,  *args, **kargs):
        HistogramLUTWidget.__init__(self, parent, *args, **kargs)
        self.item = HorizontalHistogramItem(*args, **kargs)
        self.setCentralItem(self.item)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.setMinimumHeight(95)


class HorizontalHistogramItem(HistogramLUTItem):
    """
    This is a graphicsWidget which provides controls for adjusting the display of an image.
    Includes:

    - Image histogram 
    - Movable region over histogram to select black/white levels
    - Gradient editor to define color lookup table for single-channel images
    """
    def __init__(self, image=None, fillHistogram=True):
        """
        If *image* (ImageItem) is provided, then the control will be automatically linked to the image and changes to the control will be immediately reflected in the image's appearance.
        By default, the histogram is rendered with a fill. For performance, set *fillHistogram* = False.
        """
        HistogramLUTItem.__init__(self, image, fillHistogram)

        self.layout = QtGui.QGraphicsGridLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(1,1,1,1)
        self.layout.setSpacing(0)

        self.vb = ViewBox()
        self.vb.setMaximumHeight(152)
        self.vb.setMinimumHeight(45)
        self.vb.setMouseEnabled(x=True, y=False)
        self.gradient.setOrientation('bottom')
        self.gradient.loadPreset('grey')  # TODO: load the right one here
        self.region = LinearRegionItem([0, 1], LinearRegionItem.Vertical)
        self.region.setZValue(1000)
        self.vb.addItem(self.region)
        self.axis = AxisItem('top', linkView=self.vb, maxTickLength=-10, showValues=False)
        self.layout.addItem(self.axis, 0, 0)
        self.layout.addItem(self.vb, 1, 0)
        self.layout.addItem(self.gradient, 2, 0)
        self.gradient.setFlag(self.gradient.ItemStacksBehindParent)
        self.vb.setFlag(self.gradient.ItemStacksBehindParent)

        #self.grid = GridItem()
        #self.vb.addItem(self.grid)

        self.gradient.sigGradientChanged.connect(self.gradientChanged)
        self.region.sigRegionChanged.connect(self.regionChanging)
        self.region.sigRegionChangeFinished.connect(self.regionChanged)
        self.vb.sigRangeChanged.connect(self.viewRangeChanged)

        self.plot = PlotDataItem()
        self.fillHistogram(fillHistogram)
            
        self.vb.addItem(self.plot)
        self.autoHistogramRange()
        
        if image is not None:
            self.setImageItem(image)
        #self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        
    def paint(self, p, *args):
        pen = self.region.lines[0].pen
        rgn = self.getLevels()
        p1 = self.vb.mapFromViewToItem(self, Point(rgn[0], self.vb.viewRect().center().y()))
        p2 = self.vb.mapFromViewToItem(self, Point(rgn[1], self.vb.viewRect().center().y()))
        gradRect = self.gradient.mapRectToParent(self.gradient.gradRect.rect())
        for pen in [fn.mkPen('k', width=3), pen]:
            p.setPen(pen)
            p.drawLine(p1, gradRect.topLeft())
            p.drawLine(p2, gradRect.topRight())
            p.drawLine(gradRect.topLeft(), gradRect.bottomLeft())
            p.drawLine(gradRect.topRight(), gradRect.bottomRight())
        #p.drawRect(self.boundingRect())
        
        
    def setHistogramRange(self, mn, mx, padding=0.1):
        """Set the X range on the histogram plot. This disables auto-scaling."""
        self.vb.enableAutoRange(self.vb.XAxis, False)
        self.vb.setXRange(mn, mx, padding)
