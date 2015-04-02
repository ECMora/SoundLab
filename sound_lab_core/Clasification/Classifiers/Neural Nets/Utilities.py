import os
import pickle
import numpy as np

def deserialize(filename):
    """
    Deserialize an object from a file.
    :param filename: the path to the file where the object is saved
    :return: the instance of tyhe serialized object in the file
    """
    if not os.path.exists(filename):
        raise Exception('File does not exist.')

    with open(filename, 'rb') as f:
        return pickle.load(f)

def serialize(filename, serializable_object):
    """
    Serialize an object to a file.
    :param filename: the path to the file for the object storage.
    :param object: the object to serialize.
    """
    if not filename:
        raise Exception("Invalid Path " + filename + " to save the object.")

    try:

        data_file = open(filename, 'wb')
        pickle.dump(serializable_object, data_file)
        data_file.close()

    except Exception as ex:
        print(ex.message)

def k_fold(input, target, k, randomize=True):
        indexes = np.arange(len(input))
        if randomize:
            from random import shuffle
            shuffle(indexes)

        inp = np.array([input[i] for i in np.arange(len(input))])
        tar = np.array([target[i] for i in np.arange(len(target))])

        slicesInp = [inp[i::k] for i in np.arange(k)]
        slicesTar = [tar[i::k] for i in np.arange(k)]

        for i in np.arange(k):
            validationInp = slicesInp[i]
            validationTar = slicesTar[i]
            trainingInp = [item for s in slicesInp if s is not validationInp for item in s]
            trainingTar = [item for s in slicesTar if s is not validationTar for item in s]
            yield (trainingInp,trainingTar), (validationInp, validationTar)

# for training, validation in k_fold([[1,2],[3,4],[5,6],[7,8]],[[1,2],[3,4],[5,6],[7,8]],3):
#     print(training)
#     print(validation)
