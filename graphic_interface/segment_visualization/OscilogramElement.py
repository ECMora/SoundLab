from graphic_interface.segment_visualization.VisualElement import VisualElement
from graphic_interface.segment_visualization.parameter_items.time_parameter_items.TimeParameterVisualItem import \
    TimeVisualItemWrapper
import pyqtgraph as pg


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
        VisualElement.__init__(self, number=number, signal=signal, indexFrom=indexFrom, indexTo=indexTo)

        # the time region limits
        self.element_region = pg.LinearRegionItem((self._indexFrom, self._indexTo), movable=False, brush=self.brush)

        self.element_region.mouseClickEvent = self.mouseClickEvent
        self._update_items_pos()

        self.visual_figures.append(self.element_region)

    def add_parameter_item(self, parameter_item):
        """
        Add a new measured parameter visual item into the time representation of the segment
        :param parameter_item: The TimeVisualItemWrapper to add
        :return:
        """
        if not isinstance(parameter_item, TimeVisualItemWrapper):
            raise Exception("Invalid type argument. parameter_item must be of type TimeVisualItemWrapper")

        VisualElement.add_parameter_item(self, parameter_item)

    def _update_items_pos(self):
        self.text_number.setPos(self._indexFrom / 2.0 + self._indexTo / 2.0, 0.75 * self.signal.maximumValue)
        self.element_region.setRegion((self._indexFrom, self._indexTo))
        self.element_region.setBrush(self.brush)

    def setNumber(self, n):
        """
        Updates the info in this element when its number changes.
        Is updated his instance variables and visual figures.
        @param n: The new index
        """
        VisualElement.setNumber(self, n)

        # the brush color is dependent of number
        self.element_region.setBrush(self.brush)

    def clone(self):
        return OscilogramElement(self.signal, self.indexFrom, self.indexTo, self.number)