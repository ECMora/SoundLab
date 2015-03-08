from PyQt4.QtCore import QObject


class Classifier(QObject):
    """
    Base class for the classifiers on the sound lab system
    """

    def __init__(self, name=""):
        QObject.__init__(self)
        self.name = name

    def classify(self, segment):
        pass