from PyQt4.QtCore import QObject


class OneDimensionalHandler(QObject):
    """
    Abstract base class for the handlers of each one dimensional transform.
    """

    def __init__(self, parent):
        """
            The class must have a constructor receiving one parameter: the QObject's parent.
        """
        QObject.__init__(self, parent)

    def get_transform_class(self):
        """
        Gets the class that implements the corresponding one dimensional transform.
        :return: the corresponding one dimensional transform's class
        """
        pass

    def get_transform_instance(self):
        """
        Gets a new instance of the corresponding one dimensional transform.
        :return: a new instance of the corresponding one dimensional transform's class
        """
        pass

    def get_settings(self, transform):
        """
        Gets the settings of the corresponding one dimensional transform with the values of the supplied instance.
        :param transform: the one dimensional transform instance from which to take the values
        :return: a list of dicts in the way needed to create the param tree
        """
        pass

    def get_axis_labels(self):
        """
        Gets the axis information to show
        :return: a dict with the corresponding axis labels
        """
        pass

    def get_y_default(self, transform):
        """
        Gets the axis y limits
        :param transform: the one dimensional transform instance which settings are to be changed
        :return: a tuple with the max and min y default values to show
        """
        pass

    def get_y_limits(self, transform):
        """
        Gets the axis y limits
        :param transform: the one dimensional transform instance which settings are to be changed
        :return: a tuple with the max and min y limits to show
        """
        pass

    def apply_settings_change(self, transform, change):
        """
        Applies the given change to the given transform.
        :param transform: the one dimensional transform instance which settings are to be changed
        :param change: the change to apply as a tuple (childName, _change, data) where childName is the path in the
        param tree joined by dots ('.'), change is ... and data is the new value
        """
        pass
