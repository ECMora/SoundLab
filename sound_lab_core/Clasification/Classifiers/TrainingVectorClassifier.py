from sound_lab_core.Clasification.ClassificationData import ClassificationData
from sound_lab_core.Clasification.Classifier import Classifier


class TrainingVectorClassifier(Classifier):
    """
    Represents the base class for the classifiers that
    uses training vectors
    """

    def __init__(self, name=""):
        Classifier.__init__(self, name)
