from sound_lab_core.Clasification.ClassificationData import ClassificationData
from sound_lab_core.Clasification.Classifier import Classifier


class ManualClassifier(Classifier):

    def __init__(self):
        Classifier.__init__(self, "Manual")

    def classify(self, segment, param_vector):
        return ClassificationData()