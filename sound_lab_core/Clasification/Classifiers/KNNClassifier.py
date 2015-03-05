from sound_lab_core.Clasification.ClassificationData import ClassificationData
from sound_lab_core.Clasification.Classifiers.TrainingVectorClassifier import TrainingVectorClassifier


class KNNClassifier(TrainingVectorClassifier):

    def __init__(self):
        TrainingVectorClassifier.__init__(self, "KNN")

    def classify(self, segment, param_vector=None):
        if self.training_vectors is None:
            self.get_training_vectors()

        print(param_vector)
        return ClassificationData()
