from PyQt4.QtGui import QFont
import pyqtgraph as pg

# the font size for text labels
FONT_SIZE = 13
FONT = QFont("Arial", pointSize=FONT_SIZE)


class VisualItemsCache:
    """
    Static class that handles the chache for the visual elements
    Keep a set of visual element to reuse them if necessary for efficiency
    """

    # region CONSTANTS

    free_visual_items_stack = []

    # initial Items Count
    INITIAL_REGION_ITEMS_COUNT = 500

    INITIAL_TEXT_ITEMS_COUNT = INITIAL_REGION_ITEMS_COUNT * 2

    INITIAL_GRAPH_ITEMS_COUNT = INITIAL_REGION_ITEMS_COUNT

    # the number of new items to add if the list of free items is empty
    ITEMS_GROWING_NUMBER = 100

    # endregion

    # region Release Items

    def release_visual_item(self, item):
        if item in self.graph_items:
            self.graph_items[item] = False
            self.free_graph_items_stack.append(item)

    def release_text_item(self, item):
        if item in self.text_items:
            self.text_items[item] = False
            self.free_text_items_stack.append(item)

    def release_region_item(self, item):
        if item in self.region_items:
            self.region_items[item] = False
            self.free_region_items_stack.append(item)

    # endregion

    # region Get Items

    def get_text_item(self, number):
        if len(self.free_text_items_stack) == 0:
            self.add_text_items(self.ITEMS_GROWING_NUMBER)

        item = self.free_text_items_stack.pop()
        item.setText(str(number))
        return item

    def get_region_item(self, index_from, index_to, brush):
        if len(self.free_region_items_stack) == 0:
            self.add_region_items(self.ITEMS_GROWING_NUMBER)

        item = self.free_region_items_stack.pop()
        item.setRegion((index_from, index_to))
        item.setBrush(brush)
        return item

    def get_graph_item(self):
        """

        :return:
        """
        if len(self.free_graph_items_stack) == 0:
            self.add_graph_items(self.ITEMS_GROWING_NUMBER)

        return self.free_graph_items_stack.pop()

    # endregion

    # region Create Items

    def add_text_items(self, n=None):
        """

        :param n: The number of items to add
        :return:
        """
        n = n if n is not None else self.INITIAL_TEXT_ITEMS_COUNT

        # create the text items
        for i in xrange(n):
            text_item = pg.TextItem("0", color=(255, 255, 255), anchor=(0.5, 0.5))
            text_item.setFont(FONT)
            self.text_items[text_item] = False
            self.free_text_items_stack.append(text_item)

    def add_region_items(self, n=None):
        """

        :param n: The number of items to add
        :return:
        """
        n = n if n is not None else self.INITIAL_REGION_ITEMS_COUNT

        # create the region items
        for i in xrange(n):
            region_item = pg.LinearRegionItem([0, 0], movable=False)
            self.region_items[region_item] = False
            self.free_region_items_stack.append(region_item)

    def add_graph_items(self, n=None):
        """

        :param n: The number of items to add
        :return:
        """
        n = n if n is not None else self.INITIAL_GRAPH_ITEMS_COUNT

        # create the graph items
        for i in xrange(n):
            graph_item = pg.GraphItem()
            self.graph_items[graph_item] = False
            self.free_graph_items_stack.append(graph_item)

    # endregion

    def create_items(self, n=None):
        """
        :return:
        """

        # create the text items
        self.add_text_items(n)

        # create the region items
        self.add_region_items(n)

        # create the graph items
        self.add_graph_items(n)
