# -*- coding: utf-8 -*-
from PyQt4.QtCore import QRect
from PyQt4.QtGui import QPixmap, QImage
import numpy as np
from graphic_interface.segment_visualzation.parameter_items.time_parameter_items.TimeParameterVisualItem import \
    TimeVisualItemWrapper
import pyqtgraph as pg
from sound_lab_core.Clasification.ClassificationData import ClassificationData


class ClassificationVisualItem(TimeVisualItemWrapper):

    def __init__(self):
        TimeVisualItemWrapper.__init__(self)

        # the classified specie image
        self.classification_item = pg.ImageItem()

    def get_item(self):
        return self.classification_item

    def set_data(self, signal, segment, classification_value):
        if classification_value is None or not isinstance(classification_value, ClassificationData):
            return

        self.classification_item.setToolTip(classification_value.get_full_description())

        # set the image as background
        pixmap = classification_value.get_image()

        if pixmap is None:
            return

        image = pixmap.toImage()
        if image is None:
            return

        ptr = image.bits()
        ptr.setsize(image.byteCount())
        arr = np.asarray(ptr)
        h, w = image.height(), image.width()
        depth = image.byteCount() / (w * h)
        image_array = arr.reshape((h, w, depth))

        self.classification_item.setImage(image_array)

        # set the position of the item
        left = segment.indexFrom + (segment.indexTo - segment.indexFrom) / 3.0
        top = signal.minimumValue + (signal.maximumValue - signal.minimumValue) / 5.0
        width = (segment.indexTo - segment.indexFrom) / 3.0
        height = (signal.maximumValue - signal.minimumValue) / 5.0
        self.classification_item.setRect(QRect(left, top, width, height))
