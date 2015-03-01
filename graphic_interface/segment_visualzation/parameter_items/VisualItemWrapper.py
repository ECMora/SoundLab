# -*- coding: utf-8 -*-


class VisualItemWrapper:
    """
    Represent a visual item.
    """

    def __init__(self):
        pass

    def set_data(self, signal, segment, data):
        """
        set the parameter measurement data to visualize it
        signal: Audio Signal in which the measurement was made.
        segment: The segment on the signal in which the measurement was made.
        data: value of the measurement data.
        """
        pass

    def get_item(self):
        """
        returns the visual item to include on a visual widget
        """
        return None