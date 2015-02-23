from PyQt4.QtCore import QObject
from pyqtgraph.parametertree import Parameter


class SoundLabAdapter(QObject):
    """
    Adapter Pattern Design implementation to bind
    support for segmentation classification and
    parameter measurement into the visual interface
    """

    def __init__(self):
        """
        The class must have a constructor receiving one parameter: the QObject's parent.
        """
        QObject.__init__(self)

    def get_instance(self):
        """
        Gets a new get_instance of the corresponding adapted object .
        :return: An instance of the corresponding class
        """
        return None

    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a Parameter Tree object to adapt each concrete object into the
        visual interface
        """
        return None

    def get_visual_item(self):
        """
        The instance of the visual item to include in the visual widgets
        to visualize the Object instance (if any)
        :return:
        """
        return None