from PyQt4.QtCore import QObject


class ParameterAdapter(QObject):
    """
    Abstract base class for the handlers of each one dimensional transform.
    """

    def __init__(self, parent):
        """
            The class must have a constructor receiving one parameter: the QObject's parent.
        """
        QObject.__init__(self, parent)
        self._parameter_class = None

    # region Parameter Class Property

    @property
    def parameter_class(self):
        """
        the parameter class of the adapter
        :return:
        """
        return self._parameter_class

    @parameter_class.setter
    def parameter_class(self, value):
        """
        the parameter class of the adapter
        :return:
        """
        self._parameter_class = value

    # endregion

    def get_parameter_class(self):
        """
        Gets the class that implements the corresponding parameter measurement.
        :return: the class of parameter measurement
        """
        return self.parameter_class

    def get_parameter_instance(self):
        """
        Gets a new instance of the corresponding parameter measurement.
        :return: A new instance of the corresponding parameter measurement class
        """
        return self.parameter_class()

    def get_settings(self):
        """
        Gets the settings of the corresponding parameter measurement with the values
        of the supplied instance.
        :return: a list of dicts in the way needed to create the param tree
        """
        pass