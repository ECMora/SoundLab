from PyQt4.QtGui import QFont
import pyqtgraph as pg
from graphic_interface.segments.VisualElement import VisualElement


class SpectrogramElement(VisualElement):

    def __init__(self, signal, indexFrom, indexTo, number=0):
        """
        @return:
        """
        VisualElement.__init__(self, number=number)
        self.indexFrom = indexFrom
        self.indexTo = indexTo

        # the visible text for number
        self.text_number = pg.TextItem(str(number), color=(255, 255, 255), anchor=(0.5, 0.5))
        self.text_number_pos = self.indexFrom / 2.0 + self.indexTo / 2.0, 0
        self.text_number.setPos(self.text_number_pos[0], self.text_number_pos[1])

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

    def setNumber(self, n):
        """
        Updates the info in this element when its number changes.
        Is updated his instance variables and visual figures.
        @param n: The new index
        """
        self.number = n
        self.text_number.setText(str(n))

        self.element_region.setBrush(pg.mkBrush(self.COLOR_ODD if self.number % 2 == 0 else self.COLOR_EVEN))

    def updateSpectralPosition(self, translate_time_function=None, translate_freq_function=None):
        """
        Update the visual representation of the object's visual
        spectral items to the new coordinate  system
        :type translate_freq_function: object
        :param translate_time_function: the callable that translate the
        x,y coordinate from time, frequency to the x,y indexes in spectrogram matrix
        :return:
        """
        # update the text and region
        x, y = self.text_number_pos
        x = x if translate_time_function is None else translate_time_function(x)
        y = y if translate_freq_function is None else translate_freq_function(y)
        print(self.text_number_pos, x, y)
        self.text_number.setPos(x, y)

        self.element_region.setRegion((x,y))
