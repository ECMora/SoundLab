# -*- coding: utf-8 -*-
from pyqtgraph.Qt import QtGui
import pyqtgraph.functions as fn
from pyqtgraph.Point import Point
from pyqtgraph.graphicsItems.AxisItem import AxisItem
from pyqtgraph.graphicsItems.HistogramLUTItem import HistogramLUTItem
from pyqtgraph.graphicsItems.LinearRegionItem import LinearRegionItem
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from pyqtgraph.widgets.HistogramLUTWidget import HistogramLUTWidget
import pyqtgraph as pg


class HorizontalHistogramWidget(HistogramLUTWidget):
    def __init__(self, parent=None,  *args, **kargs):
        HistogramLUTWidget.__init__(self, parent, *args, **kargs)
        self.item = HorizontalHistogramItem(*args, **kargs)
        self.setCentralItem(self.item)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.setMinimumHeight(95)


    def restoreState(self, colorBarState):
        """
        Restore the state of the histogram values form the color bar supplied
        :param colorBarState:
        :return:
        """
        self.item.restoreState(colorBarState)

    def setRegion(self, region):
        """
        Update the current visualization trheshold region with the supplied
        :param region:
        :return:
        """
        self.item.setRegion(region)

    @property
    def region(self):
        """
        :return: the current selected threshold region
        """
        return self.item._region

    @property
    def gradient(self):
        """
        The gradient of the histogfram item
        """
        return self.item.gradient


class HorizontalHistogramItem(HistogramLUTItem):
    """
    This is a graphicsWidget which provides controls for adjusting the display of an image.
    Includes:

    - Image histogram 
    - Movable region over histogram to select black/white levels
    - Gradient editor to define color lookup table for single-channel images
    """
    # CONSTANTS
    # the minThresholdLabel and maxThresholdLabel heigth of the histogram widget
    HISTOGRAM_MAX_HEIGHT = 152
    HISTOGRAM_MIN_HEIGHT = 45
    DECIMAL_PLACES = 2

    def __init__(self, image=None, fillHistogram=True):
        """
        If *image* (ImageItem) is provided, then the control will be automatically linked
        to the image and changes to the control will be immediately reflected in the image's appearance.
        By default, the histogram is rendered with a fill. For performance, set *fillHistogram* = False.
        """
        HistogramLUTItem.__init__(self, image, fillHistogram)

        self.layout = QtGui.QGraphicsGridLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(0)

        # the viewbox in which would be displayed the histogram
        # get a new and descriptive name for the view box
        self.view_boxHistogram = self.vb
        self.view_boxHistogram = ViewBox()
        self.view_boxHistogram.setMaximumHeight(self.HISTOGRAM_MAX_HEIGHT)
        self.view_boxHistogram.setMinimumHeight(self.HISTOGRAM_MIN_HEIGHT)
        self.view_boxHistogram.setMouseEnabled(x=False, y=False)

        # set defaults gradient position and color bar
        self.gradient.setOrientation('bottom')
        self.gradient.loadPreset('thermal')

        # todo remove this parche the region of threshold selection
        self.region.setVisible(False)
        self._region = LinearRegionItem(values=[-40, 0], orientation=LinearRegionItem.Vertical)


        self.view_boxHistogram.addItem(self._region)
        self.axis = AxisItem('top', linkView=self.view_boxHistogram, maxTickLength=-10, showValues=False)

        self.layout.addItem(self.axis, 0, 0)
        self.layout.addItem(self.view_boxHistogram, 1, 0)
        self.layout.addItem(self.gradient, 2, 0)

        self.gradient.setFlag(self.gradient.ItemStacksBehindParent)
        self.view_boxHistogram.setFlag(self.gradient.ItemStacksBehindParent)

        self.plot = PlotDataItem()
        self.fillHistogram(fillHistogram)

        self.view_boxHistogram.addItem(self.plot)
        self.autoHistogramRange()

        # set the fixed range of visualization
        self.view_boxHistogram.setXRange(-120, 5)
        self._region.setBounds((-120, 5))

        y_range = self.view_boxHistogram.viewRange()[1]

        # the minThresholdLabel and maxThresholdLabel labels
        self.minThresholdLabel = pg.TextItem(self.tr(u'Min'), color=(255, 255, 255), anchor=(1, 0.5))
        self.view_boxHistogram.addItem(self.minThresholdLabel)

        self.maxThresholdLabel = pg.TextItem(self.tr(u'Max'), color=(255, 255, 255), anchor=(0, 0.5))
        self.view_boxHistogram.addItem(self.maxThresholdLabel)

        self.gradient.sigGradientChanged.connect(self.gradientChanged)
        self._region.sigRegionChanged.connect(self.regionChanging)
        self._region.sigRegionChangeFinished.connect(self.regionChanged)

        labels_ypos = self.view_boxHistogram.viewRange()[1][1] * 0.7
        self.maxThresholdLabel.setPos(self._region.getRegion()[1], labels_ypos)
        self.minThresholdLabel.setPos(self._region.getRegion()[0], labels_ypos)

        # update the tooltips and position of the limit labels
        self._region.sigRegionChangeFinished.connect(
            lambda: self.maxThresholdLabel.setToolTip(self.tr(u'Max Threshold') + u": " +
                                                      unicode(round(self._region.getRegion()[1],
                                                                    self.DECIMAL_PLACES))))

        self._region.sigRegionChangeFinished.connect(
            lambda: self.minThresholdLabel.setToolTip(self.tr(u'Min Threshold') + u": " +
                                                      unicode(round(self._region.getRegion()[0],
                                                                    self.DECIMAL_PLACES))))

        # set the y position of the labels to the 70% of the visible y range of the viewbox
        self._region.sigRegionChanged.connect(
            lambda: self.maxThresholdLabel.setPos(self._region.getRegion()[1],
                                                  self.view_boxHistogram.viewRange()[1][1] * 0.7))

        self._region.sigRegionChanged.connect(
            lambda: self.minThresholdLabel.setPos(self._region.getRegion()[0],
                                                  self.view_boxHistogram.viewRange()[1][1] * 0.7))

        if image is not None:
            self.setImageItem(image)

        self.setLayout(self.layout)

        # self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)

    def paint(self, p, *args):
        """

        :param p:
        :param args:
        :return:
        """
        pen = self._region.lines[0].pen
        rgn = self._region.getRegion()
        p1 = self.view_boxHistogram.mapFromViewToItem(self, Point(rgn[0], self.view_boxHistogram.viewRect().center().y()))
        p2 = self.view_boxHistogram.mapFromViewToItem(self, Point(rgn[1], self.view_boxHistogram.viewRect().center().y()))
        gradRect = self.gradient.mapRectToParent(self.gradient.gradRect.rect())
        for pen in [fn.mkPen('k', width=3), pen]:
            p.setPen(pen)
            p.drawLine(p1, gradRect.topLeft())
            p.drawLine(p2, gradRect.topRight())
            p.drawLine(gradRect.topLeft(), gradRect.bottomLeft())
            p.drawLine(gradRect.topRight(), gradRect.bottomRight())

    def setHistogramRange(self, mn, mx, padding=0.1):
        """Set the X range on the histogram plot. This disables auto-scaling."""
        self.view_boxHistogram.enableAutoRange(self.view_boxHistogram.XAxis, False)
        self.view_boxHistogram.setXRange(mn, mx, padding)

    def restoreState(self, colorBarState):
        """
        Restore the state of the histogram values form the color bar supplied
        :param colorBarState:
        :return:
        """
        self.gradient.restoreState(colorBarState)

    def setRegion(self,region):
        """
        Update the current visualization trheshold region with the supplied
        :param region:
        :return:
        """
        self._region.setRegion(region)

    def regionChanged(self):
        self.sigLevelChangeFinished.emit(self)

    def regionChanging(self):
        if self.imageItem is not None:
            self.imageItem.setLevels(self._region.getRegion())
        self.sigLevelsChanged.emit(self)
        self.update()