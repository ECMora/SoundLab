from sound_lab_core.Clasification.ClassificationData import ClassificationData
from sound_lab_core.Clasification.Classifier import Classifier


class TrainingVector:

    def __init__(self):
        pass


class TrainingVectorClassifier(Classifier):
    """
    Represents the base class for the classifiers that
    uses training vectors
    """

    def __init__(self, name=""):
        Classifier.__init__(self, name)

        # the current training vectors list to make classification
        # each element on list is a Training Vector
        # measured.
        self.training_vectors = None

        # the list of parameter adapter that would be used for classification
        self._parameters = []

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameter_measurements_list):
        self._parameters = parameter_measurements_list
        self.training_vectors = None

    def get_training_vectors(self):
        """
        load from db the training vectors according to the
        parameters list supplied
        :return:
        """
        if len(self.parameters) == 0:
            self.training_vectors = []