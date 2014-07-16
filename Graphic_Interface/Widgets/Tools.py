# -*- coding: utf-8 -*-
import pyqtgraph as pg

class Tools:
    """
    the tools for interaction with the signal in the QSignalVisualizerWidget.
    """
    Zoom,RectangularCursor,CircularEraser,RectangularEraser,PointerCursor, OscilogramThreshold = range(6)

class RectROI(pg.ROI):
    def __init__(self, pos, size, centered=False, sideScalers=False, **args):
        #QtGui.QGraphicsRectItem.__init__(self, 0, 0, size[0], size[1])
        pg.ROI.__init__(self, pos, size, **args)
        if centered:
            center = [0.5, 0.5]
        else:
            center = [0, 0]
        if sideScalers:
            self.addScaleHandle([1, 0.5], [center[0], 0.5])
            self.addScaleHandle([0.5, 1], [0.5, center[1]])
