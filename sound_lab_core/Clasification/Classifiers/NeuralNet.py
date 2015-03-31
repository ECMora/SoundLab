import os
from neurolab.trans import LogSig, SoftMax, TanSig, PureLin
from neurolab.train import train_bfgs, train_gdm, train_rprop, train_gdx
from neurolab.error import MSE, SSE, MAE, CEE, SAE
from neurolab.layer import Perceptron
from neurolab.init import initnw, InitRand
from neurolab.core import Net
import numpy as np
import pickle

class TransfFunctions:
    """
    Enum class for neurolab activation functions wrapper
    """
    SIGMOID = LogSig
    SOFTMAX = SoftMax
    TANH = TanSig
    LIN = PureLin

class TrainMethods:
    """
    Enum class for neurolab train functions wrapper
    """
    GDM = train_gdm
    GDX = train_gdx
    RPROP = train_rprop
    BFGS = train_bfgs

class ErrorFunctions:
    """
    Enum class for neurolab error functions wrapper
    """
    MSE = MSE
    SSE = SSE
    SAE = SAE
    CEE = CEE
    MAE = MAE

# TODO set the max and min values
class NeuralNet():

    def __init__(self, minmax, identificationClasses, paramsList, dimList, transf=None, trainf = TrainMethods.GDX, errorf = ErrorFunctions.MSE):
        """
        Initializes a neural network with the specified structure and functionality parameters
        :param minmax: list with min and max parameters values
        :param identificationClasses: list of identification classes names
        :param paramsList: parameters adapters class references
        :param dimList: list with each network layer dimension
        :param activList: list of each network layer activation functions
        :param trainf: training function
        :param errorf: error function
        """
        self._minmax = minmax
        self._params = paramsList
        self._classes = identificationClasses
        self._targetVectors = self.get_classes_vectors()

        net_ci = len(minmax)
        net_co = dimList[-1]

        if transf is None:
            transf = [TransfFunctions.SIGMOID()] * len(dimList)
        assert len(transf) == len(dimList)

        layers = []
        for i, nn in enumerate(dimList):
            layer_ci = dimList[i - 1] if i > 0 else net_ci
            l = Perceptron(layer_ci, nn, transf[i])
            l.initf = initnw
            layers.append(l)
        connect = [[i - 1] for i in range(len(layers) + 1)]

        self._net = Net(minmax, net_co, layers, connect, trainf, errorf())

    #region Save and Load

    @staticmethod
    def save(serializable_object, filename):
        if not filename:
            raise Exception("Invalid Path " + filename + " to save the neural net.")

        try:
            data_file = open(filename, 'wb')
            pickle.dump(serializable_object, data_file)
            data_file.close()

        except Exception as ex:
            print(ex.message)

    @staticmethod
    def load(filename):
        if not os.path.exists(filename):
            raise Exception('File does not exist.')

        with open(filename, 'rb') as f:
            return pickle.load(f)

    #endregion

    #region Params and classes Properties

    @property
    def classes(self):
        """
        Classes that identifies the neural net
        :return: list of classes names
        """
        return self._classes

    @property
    def params(self):
        """
        The parameters adapters list used as features
        :return: adapters list
        """
        return self._params

    #endregion

    def getClassifierInfo(self):
        return {u'params' : self._params, u'classes': self._classes}

    def get_classes_vectors(self):
        """
        Build the target vectors to use in the network according to predefined classes set
        :return:
        """
        return np.identity(len(self.classes)).clip(0.1, 0.9)

    def train(self, training_vectors, epochs = 500, learningRate=.01, momentum=.9):

        # building the measures vectors to numpy arrays
        if not isinstance(training_vectors[0], np.ndarray):
            XtrnData = np.array(training_vectors[0])
        else:XtrnData = training_vectors[0]
        YtrnData = None

        # setting the class vectors to training
        for vClass in training_vectors[1]:
            index = self.classes.index(vClass)
            if YtrnData is None:
                YtrnData = np.array([self._targetVectors[index]])
            else:
                YtrnData = np.concatenate((YtrnData, np.array([self._targetVectors[index]])))

        # starting the training
        errors = self._net.train(XtrnData, YtrnData, epochs=epochs, show=100, goal=0.01, lr=learningRate,
                                 mc=momentum)

        # returns the last executed epoch error
        return errors[-1]

    def train_crossValidation(self, trainingVectors, validationSet, maxEpochs=500, continueEpochs=100,
                              learningRate=.3, momentum=.9):
        pass

    def classify(self, paramVector):
        """
        Performs the classification process over a pre trained network and returns the
        output class and accuracy percent
        :param paramVector: list of measured parameters values
        :return: output class, accuracy percent
        """
        if not isinstance(paramVector, np.ndarray):
            paramVector = np.array(paramVector)
        output = self._net.sim([paramVector])
        index = output.argmax()

        # target = np.zeros(output.shape).clip(0.1)
        # target[index] += 0.8

        target = self._targetVectors[index]

        percent = self._net.errorf(target, output)
        return self._classes[index], percent

