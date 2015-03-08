from sound_lab_core.Clasification.ClassificationData import ClassificationData
from sound_lab_core.Clasification.Classifiers.TrainingVectorClassifier import TrainingVectorClassifier, TrainingVector


class KNNClassifier(TrainingVectorClassifier):

    def __init__(self):
        TrainingVectorClassifier.__init__(self, "KNN")
        self._k = 1

    @property
    def k(self):
        """
        The number of neighborhood vectors to compare with
        :return:
        """
        return self._k

    def distance(self, training_vector1, training_vector2):
        """
        Implementation of distance metrics over the space of training vectors
        :param training_vector1:
        :param training_vector2:
        :return:
        """
        if training_vector1 is None or training_vector2 is None or training_vector1.values is None \
           or training_vector2.values is None or len(training_vector1.values) != len(training_vector2.values):
            raise Exception("Invalid Arguments")

        return sum([(training_vector1.values[i] - training_vector2.values[i]) ** 2
                    for i in xrange(len(training_vector1.values))]) ** 0.5

    def get_classification(self, training_vector_list):
        """

        :param training_vector_list:
        :return:
        """
        return training_vector_list[0].identification

    def classify(self, segment, param_vector=None):
        if len(self.training_vectors) == 0:
            return ClassificationData()

        try:
            param_vector = TrainingVector(values=param_vector)

            distance_array = [self.distance(param_vector, x) for x in self.training_vectors]

            sorted_array = [(distance_array[i], self.training_vectors[i]) for i in xrange(len(distance_array))]

            sorted_array.sort(lambda x, y: 1 if x[0] < y[0] else 1)

            if self.k > len(sorted_array):
                return self.get_classification([x[1] for x in sorted_array])

            return self.get_classification([sorted_array[i][1] for i in xrange(self.k)])

        except Exception as ex:
            print("Errors on KNN classification. " + ex.message)
            return ClassificationData()
