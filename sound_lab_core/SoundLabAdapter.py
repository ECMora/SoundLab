from PyQt4.QtCore import QObject
from pyqtgraph.parametertree import Parameter


class SoundLabAdapter(QObject):
    """

    """

    def __init__(self, parent):
        """
            The class must have a constructor receiving one parameter: the QObject's parent.
        """
        QObject.__init__(self, parent)

    def get_instance(self):
        """
        Gets a new get_instance of the corresponding adapted object .
        :return: A new get_instance of the corresponding class
        """
        return None

    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a list of dicts in the way needed to create the param tree
        """
        return None

    def get_visual_item(self):
        """
        The instance of the visual item to include for visualization
        :return:
        """
        return None

    def apply_settings_change(self, transform, change):
        pass