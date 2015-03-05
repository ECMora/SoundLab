

class Classifier:
    """
    Base class for the classifiers on the sound lab system
    """

    def __init__(self, name=""):
        self.name = name

    def classify(self, segment):
        pass