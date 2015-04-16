from collections import deque
from duetto.audio_signals.AudioSignal import AudioSignal
from graphic_interface.segment_visualization.DetectedSoundLabElement import DetectedSoundLabElement


class VisualItemsCache:
    """
    Static class that handles the cache for the visual elements
    Keep in memory a set of visual element to reuse them if necessary for efficiency
    Singleton pattern.
    """

    class __Singleton:

        # region CONSTANTS
        # static signal to initialize elements
        signal = AudioSignal()

        free_visual_items_queue = deque()

        # initial Items Count
        INITIAL_ITEMS_COUNT = 250

        # the number of new items to add if the list of free items is empty
        ITEMS_GROWING_NUMBER = 50

        # endregion

        def __init__(self):
            self.add_visual_items()

        def release_visual_item(self, item):
            self.free_visual_items_queue.append(item)

        def get_visual_item(self, signal, index_from, index_to, number=0, signal_callback=None):
            """

            :param number:
            :return:
            """
            if len(self.free_visual_items_queue) == 0:
                self.add_visual_items(self.ITEMS_GROWING_NUMBER)

            # return the item requested
            item = self.free_visual_items_queue.pop()
            item.set_signal(signal)
            item.set_bounds(index_from, index_to)
            item.setNumber(number)
            item.set_element_clicked_callback(signal_callback)

            return item

        def add_visual_items(self, n=None):
            """
            :param n: The number of items to add
            :return:
            """
            n = n if n is not None else self.INITIAL_ITEMS_COUNT

            # create the text items
            for i in xrange(n):
                item = DetectedSoundLabElement(self.signal, 0, 0)
                self.free_visual_items_queue.append(item)

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
