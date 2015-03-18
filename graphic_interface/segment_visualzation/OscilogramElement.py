from graphic_interface.segment_visualzation.VisualElement import VisualElement
from graphic_interface.segment_visualzation.parameter_items.time_parameter_items.TimeParameterVisualItem import \
    TimeVisualItemWrapper


class OscilogramElement(VisualElement):
    """
    Class that represents the time visualization of a detected segment
    """

    def __init__(self, signal, indexFrom, indexTo, number=0):
        """
        :type indexFrom: object
        :type signal: AudioSignal
        @return:
        """
        VisualElement.__init__(self, number=number)

        self.indexFrom = indexFrom
        self.indexTo = indexTo

        self.text_number.setPos(self.indexFrom / 2.0 + self.indexTo / 2.0, 0.75 * signal.maximumValue)

        # the time region limits
        self.element_region = VisualElement.visual_items_cache.get_region_item(self.indexFrom, self.indexTo, self.brush)

        self.element_region.mouseClickEvent = self.mouseClickEvent

        self.visual_figures.append([self.element_region, True])

    def release_resources(self):
        VisualElement.visual_items_cache.release_text_item(self.text_number)
        VisualElement.visual_items_cache.release_region_item(self.element_region)

    def add_parameter_item(self, parameter_item):
        """
        Add a new measured parameter visual item into the time representation of the segment
        :param parameter_item: The TimeVisualItemWrapper to add
        :return:
        """
        if not isinstance(parameter_item, TimeVisualItemWrapper):
            raise Exception("Invalid type argument. parameter_item must be of type TimeVisualItemWrapper")

        VisualElement.add_parameter_item(self, parameter_item)

    def setNumber(self, n):
        """
        Updates the info in this element when its number changes.
        Is updated his instance variables and visual figures.
        @param n: The new index
        """
        VisualElement.setNumber(self, n)

        # the brush color is dependent of number
        self.element_region.setBrush(self.brush)