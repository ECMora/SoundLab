from PyQt4.QtGui import QFont
import pyqtgraph as pg
from graphic_interface.segments.VisualElement import VisualElement
from graphic_interface.segments.parameter_items.time_parameter_items.TimeParameterVisualItem import \
    TimeParameterVisualItem


class OscilogramElement(VisualElement):

    def __init__(self, signal, indexFrom, indexTo, number=0):
        """
        @return:
        """
        VisualElement.__init__(self, number=number)
        self.indexFrom = indexFrom
        self.indexTo = indexTo

        # the visible text for number
        self.text_number = pg.TextItem(str(number), color=(255, 255, 255), anchor=(0.5, 0.5))
        self.text_number.setPos(self.indexFrom / 2.0 + self.indexTo / 2.0, 0.75 * signal.maximumValue)

        font = QFont()
        font.setPointSize(13)
        self.text_number.setFont(font)

        color = self.COLOR_ODD if self.number % 2 == 0 else self.COLOR_EVEN
        self.element_region = pg.LinearRegionItem([self.indexFrom, self.indexTo],
                                                  movable=False, brush=(pg.mkBrush(color)))
        self.element_region.mouseClickEvent = self.mouseClickEvent

        # update the visual representation
        self.visual_figures.append([self.element_region, True])  # item visibility
        self.visual_text.append([self.text_number, True])

    def addParameterItem(self, parameter_item):
        if not isinstance(parameter_item, TimeParameterVisualItem):
            raise Exception("Invalid type argument. parameter_item must be of type TimeParameterVisualItem")

        VisualElement.addParameterItem(self, parameter_item)

    def setNumber(self, n):
        """
        Updates the info in this element when its number changes.
        Is updated his instance variables and visual figures.
        @param n: The new index
        """
        VisualElement.setNumber(self, n)
        self.text_number.setText(str(n))
        self.element_region.setBrush(pg.mkBrush(self.COLOR_ODD if self.number % 2 == 0 else self.COLOR_EVEN))