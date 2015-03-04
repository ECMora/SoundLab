from sound_lab_core.Clasification.Classifiers.TrainingVectorClassifier import TrainingVectorClassifier


class KNNClassifier(TrainingVectorClassifier):

    def __init__(self):
        TrainingVectorClassifier.__init__(self, "KNN")
