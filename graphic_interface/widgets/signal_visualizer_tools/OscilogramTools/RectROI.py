# -*- coding: utf-8 -*-
import pyqtgraph as pg


class RectROI(pg.ROI):
    def __init__(self, pos, size, centered=False, sideScalers=False, **args):
        pg.ROI.__init__(self, pos, size, **args)
        if centered:
            center = [0.5, 0.5]
        else:
            center = [0, 0]
        if sideScalers:
            self.addScaleHandle([1, 0.5], [center[0], 0.5])
            self.addScaleHandle([0.5, 1], [0.5, center[1]])
