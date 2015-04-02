from sound_lab_core.Clasification.Classifiers.TrainingVectorClassifier import TrainingVectorClassifier
from sound_lab_core.Clasification.ClassificationData import ClassificationData
import numpy as np


# TODO set the training vectors according the context classifier parameters
class NeuralNetsClassifier(TrainingVectorClassifier):

    def __init__(self, params, familyNet=None, genusNet=None, specieNet=None):

        TrainingVectorClassifier.__init__(self, "Neural Nets")

        # load nets
        self._family = familyNet
        self._genus = genusNet
        self._specie = specieNet
        self._params = params
        self._parameters = None

    #region Family, Genus and Specie properties
    @property
    def familyNet(self):
        return self._family

    @property
    def genusNet(self):
        return self._genus

    @property
    def specieNet(self):
        return self._specie
    #endregion

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    def classify(self, segment, param_vector):

        specie = None
        genus = None
        family = None

        if self.specieNet is not None:
            vector = self.get_params_set(self.specieNet.params, param_vector)
            specie, sPercent = self.specieNet.classify(vector)
        if self.genusNet is not None:
            vector = self.get_params_set(self.genusNet.params, param_vector)
            genus, gPercent = self.genusNet.classify(vector)
        if self.familyNet is not None:
            vector = self.get_params_set(self.familyNet.params, param_vector)
            family, fPercent = self.familyNet.classify(vector)

        #TODO classify according to certainly percent from taxonomy contexts classifiers
        return ClassificationData(specie=specie, genus=genus, family=family)

    def get_params_set(self, classSet, vectorSet):

        vector = []

        for param in classSet:
            try:
                index = self._params.index(param)
                vector.append(vectorSet[index])

            except ValueError:
                continue

        return vector