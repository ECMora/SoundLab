from PyQt4.QtCore import QObject


class SoundLabAdapter(QObject):
    """

    """

    def __init__(self, parent):
        """
            The class must have a constructor receiving one parameter: the QObject's parent.
        """
        QObject.__init__(self, parent)

        # the class to be adapted to
        self._adapted_class = None

    # region Parameter Class Property

    @property
    def adapted_class(self):
        """
        the parameter class of the adapter
        :return:
        """
        return self._adapted_class

    @adapted_class.setter
    def adapted_class(self, value):
        """
        the parameter class of the adapter
        :return:
        """
        self._adapted_class = value

    # endregion

    def get_instance(self):
        """
        Gets a new instance of the corresponding parameter measurement.
        :return: A new instance of the corresponding parameter measurement class
        """
        return self.adapted_class()

    def get_settings(self):
        """
        Gets the settings of the corresponding adapted class.
        :return: a list of dicts in the way needed to create the param tree
        """
        return []

    def apply_settings_change(self, transform, change):
        pass