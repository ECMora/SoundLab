import numpy as np
from graphic_interface.segment_visualzation.VisualElement import VisualElement
from graphic_interface.segment_visualzation.parameter_items.spectral_parameter_items.SpectralParameterVisualItem import \
    SpectralVisualItemWrapper


class SpectrogramElement(VisualElement):
    """
    The spectral visual representation of a detected segment
    """

    def __init__(self, signal, indexFrom, indexTo, number=0):
        VisualElement.__init__(self, number=number)
        self.indexFrom = indexFrom
        self.indexTo = indexTo

        max_freq = signal.samplingRate / 2.0

        # the visible text for number
        self.text_number_pos = self.indexFrom / 2.0 + self.indexTo / 2.0, max_freq * 0.9
        self.text_number.setPos(self.text_number_pos[0], self.text_number_pos[1])

        self.element_region = VisualElement.visual_items_cache.get_graph_item()

        self.element_region.mouseClickEvent = self.mouseClickEvent

        # Define positions of nodes
        self.element_region_pos = np.array([
            [self.indexFrom, max_freq * 0.8],
            [self.indexFrom, max_freq * 0.85],
            [self.indexTo, max_freq * 0.85],
            [self.indexTo, max_freq * 0.8]
        ])

        self.element_region_adj = np.array([[0, 1], [1, 2], [2, 3]])

        # update the visual representation
        self.visual_figures.append([self.element_region, True])  # item visibility

    def release_resources(self):
        VisualElement.visual_items_cache.release_text_item(self.text_number)
        VisualElement.visual_items_cache.release_graph_item(self.element_region)

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

        for item, visibility in self.visual_parameters_items:
            item.translate_time_freq_coords(translate_time_function, translate_freq_function)