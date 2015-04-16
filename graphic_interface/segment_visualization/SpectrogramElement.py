import numpy as np
from graphic_interface.segment_visualization.VisualElement import VisualElement
from graphic_interface.segment_visualization.parameter_items.spectral_parameter_items.SpectralParameterVisualItem import \
    SpectralVisualItemWrapper
import pyqtgraph as pg


class SpectrogramElement(VisualElement):
    """
    The spectral visual representation of a detected segment
    """

    def __init__(self, signal, indexFrom, indexTo, number=0):
        VisualElement.__init__(self, number=number, signal=signal,indexFrom=indexFrom, indexTo=indexTo)

        self.element_region = pg.GraphItem()
        self.element_region.mouseClickEvent = self.mouseClickEvent

        # Define positions of nodes
        self.element_region_pos = np.array([])
        self.element_region_adj = np.array([[0, 1], [1, 2], [2, 3]])
        self._update_items_pos()

        # update the visual representation
        self.visual_figures.append(self.element_region)  # item visibility

    def _update_items_pos(self):
        self.text_number_pos = self._indexFrom / 2.0 + self._indexTo / 2.0, self.signal.samplingRate * 0.9 / 2.0
        self.text_number.setPos(self.text_number_pos[0], self.text_number_pos[1])
        max_freq = self.signal.samplingRate / 2.0
        self.element_region_pos = np.array([
            [self._indexFrom, max_freq * 0.8],
            [self._indexFrom, max_freq * 0.85],
            [self._indexTo, max_freq * 0.85],
            [self._indexTo, max_freq * 0.8]
        ])

    def setNumber(self, n):
        """
        Updates the info in this element when its number changes.
        Is updated his instance variables and visual figures.
        @param n: The new index
        """
        VisualElement.setNumber(self, n)

        # the color is dependent of number
        self.element_region.setData(pen=self.pen)

    def add_parameter_item(self, parameter_item):
        # check the type of the added parameter items as SpectralVisualItemWrapper
        if not isinstance(parameter_item, SpectralVisualItemWrapper):
            raise Exception("Invalid type argument. parameter_item must be of type SpectralVisualItemWrapper")

        VisualElement.add_parameter_item(self, parameter_item)

    def translate_time_freq_coords(self, translate_time_function=None, translate_freq_function=None):
        """
        Update the visual representation of the object's visual
        spectral items to the new coordinate  system
        :type translate_freq_function: object
        :param translate_time_function: the callable that translate the
        x,y coordinate from time, frequency to the x,y indexes in spectrogram matrix
        :return:
        """
        # update the text label
        x, y = self.text_number_pos
        x = x if translate_time_function is None else translate_time_function(x)
        y = y if translate_freq_function is None else translate_freq_function(y)

        self.text_number.setPos(x, y)
        
        # update the region delimiter
        pos = np.zeros(len(self.element_region_pos) * 2).reshape((len(self.element_region_pos), 2))

        for i in range(len(self.element_region_pos)):
            if translate_time_function is not None:
                pos[i, 0] = translate_time_function(self.element_region_pos[i, 0])

            if translate_freq_function is not None:
                pos[i, 1] = translate_freq_function(self.element_region_pos[i, 1])
        
        options = dict(size=1, symbol='d', pxMode=False, pen=self.pen)
        self.element_region.setData(pos=pos, adj=self.element_region_adj, **options)

        for item in self.visual_parameters_items:
            item.translate_time_freq_coords(translate_time_function, translate_freq_function)