from PyQt4.QtCore import QObject


class SoundLabAdapter(QObject):
    """

    """

    def __init__(self, parent):
        """
            The class must have a constructor receiving one parameter: the QObject's parent.
        """
        QObject.__init__(self, parent)

    @property
    def instance(self):
        """
        Gets a new instance of the corresponding adapted object .
        :return: A new instance of the corresponding class
        """
        return None


    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a list of dicts in the way needed to create the param tree
        """
        return None

    def apply_settings_change(self, transform, change):
        pass