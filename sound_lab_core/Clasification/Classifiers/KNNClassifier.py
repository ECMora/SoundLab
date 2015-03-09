from sound_lab_core.Clasification.ClassificationData import ClassificationData
from sound_lab_core.Clasification.Classifiers.TrainingVectorClassifier import TrainingVectorClassifier, TrainingVector


class KNNClassifier(TrainingVectorClassifier):
    """
    Implementation of K nearest neighborhood classification method
    """

    def __init__(self, k=1):
        TrainingVectorClassifier.__init__(self, "KNN")

        # the number of neighborhoods to use to compare
        self._k = k

    @property
    def k_value(self):
        """
        The number of neighborhood vectors to compare with
        :return:
        """
        return self._k

    def distance(self, vector1, vector2):
        """
        Implementation of distance metrics over the space of training vectors
        :return:
        """
        if vector1 is None or vector2 is None or vector1.values is None \
           or vector2.values is None or len(vector1.values) != len(vector2.values):
            raise Exception("Invalid Arguments")

        # simple euclidean distance
        return sum([(vector1.values[i] - vector2.values[i]) ** 2
                    for i in xrange(len(vector1.values))]) ** 0.5

    def get_classification(self, training_vector_list):
        """
        Method that compute the classification given the k vectors identified.
        Implements the logic to extract the classification
        :param training_vector_list: The list of k_value nearest training vectors
        :return:
        """
        if training_vector_list is None or len(training_vector_list) == 0:
            return ClassificationData()

        return training_vector_list[0].identification

    def classify(self, segment, param_vector=None):
        if len(self.training_vectors) == 0 or param_vector is None:
            return ClassificationData()

        try:
            param_vector = TrainingVector(values=param_vector)

            # measure the distance to each of the training vectors
            distance_array = [self.distance(param_vector, x) for x in self.training_vectors]

            # sort to get the first k_value
            sorted_array = [(distance_array[i], self.training_vectors[i]) for i in xrange(len(distance_array))]
            sorted_array.sort(lambda x, y: 1 if x[0] < y[0] else 1)

            if self.k_value > len(sorted_array):
                return self.get_classification([x[1] for x in sorted_array])

            return self.get_classification([sorted_array[i][1] for i in xrange(self.k_value)])

        except Exception as ex:
            print("Errors on KNN classification. " + ex.message)
            return ClassificationData()
