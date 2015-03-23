from PyQt4.QtGui import QFont
import pyqtgraph as pg
from collections import deque


class VisualItemsCache:
    """
    Static class that handles the cache for the visual elements
    Keep in memory a set of visual element to reuse them if necessary for efficiency
    Singleton pattern.
    """

    class __Singleton:

        # region CONSTANTS

        # the font size for text labels
        FONT_SIZE = 13
        FONT = QFont("Arial", pointSize=FONT_SIZE)  # the queue with free items

        free_text_items_queue = deque()

        # the queue with free items
        free_graph_items_queue = deque()

        # the queue with free items
        free_region_items_queue = deque()

        # initial Items Count
        INITIAL_REGION_ITEMS_COUNT = 1000

        INITIAL_TEXT_ITEMS_COUNT = INITIAL_REGION_ITEMS_COUNT * 2

        INITIAL_GRAPH_ITEMS_COUNT = INITIAL_REGION_ITEMS_COUNT

        # the number of new items to add if the list of free items is empty
        ITEMS_GROWING_NUMBER = 500

        # endregion

        def __init__(self):
            self.create_items()

        # region Release Items

        def release_graph_item(self, item):
            self.free_graph_items_queue.append(item)

        def release_text_item(self, item):
            self.free_text_items_queue.append(item)

        def release_region_item(self, item):
            self.free_region_items_queue.append(item)

        # endregion

        # region Get Items

        def get_text_item(self, number=0):
            """

            :param number:
            :return:
            """
            if len(self.free_text_items_queue) == 0:
                self.add_text_items(self.ITEMS_GROWING_NUMBER)

            # return the text item requested
            item = self.free_text_items_queue.pop()
            item.setText(str(number))
            return item

        def get_region_item(self, index_from, index_to, brush):
            """

            :param index_from:
            :param index_to:
            :param brush:
            :return:
            """
            if len(self.free_region_items_queue) == 0:
                self.add_region_items(self.ITEMS_GROWING_NUMBER)

            # return the region item requested
            item = self.free_region_items_queue.pop()
            item.setRegion((index_from, index_to))
            item.setBrush(brush)
            return item

        def get_graph_item(self):
            """
            :return: A graph item.
            """
            if len(self.free_graph_items_queue) == 0:
                self.add_graph_items(self.ITEMS_GROWING_NUMBER)

            return self.free_graph_items_queue.pop()

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
                text_item.setFont(self.FONT)
                self.free_text_items_queue.append(text_item)

        def add_region_items(self, n=None):
            """

            :param n: The number of items to add
            :return:
            """
            n = n if n is not None else self.INITIAL_REGION_ITEMS_COUNT

            # create the region items
            for i in xrange(n):
                region_item = pg.LinearRegionItem([0, 0], movable=False)
                self.free_region_items_queue.append(region_item)

        def add_graph_items(self, n=None):
            """

            :param n: The number of items to add
            :return:
            """
            n = n if n is not None else self.INITIAL_GRAPH_ITEMS_COUNT

            # create the graph items
            for i in xrange(n):
                graph_item = pg.GraphItem()
                self.free_graph_items_queue.append(graph_item)

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

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if VisualItemsCache.__instance is None:
            # Create and remember instance
            VisualItemsCache.__instance = VisualItemsCache.__Singleton()

        # Store instance reference as the only member in the handle
        self.__dict__['_VisualItemsCache__instance'] = VisualItemsCache.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
