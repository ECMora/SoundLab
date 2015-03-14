from sound_lab_core.Clasification.ClassificationData import ClassificationData
from sound_lab_core.Clasification.Classifiers.TrainingVectorClassifier import TrainingVectorClassifier, TrainingVector
import heapq as heap


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
            priority_queue = []

            for vector in self.training_vectors:
                if len(priority_queue) < self.k_value:
                    heap.heappush(priority_queue, self.distance(param_vector, vector))

                else:
                    heap.heappushpop(priority_queue, self.distance(param_vector, vector))

            indexes = [k for k in xrange(len(priority_queue))]

            return self.get_classification([self.training_vectors[i] for i in indexes])

        except Exception as ex:
            print("Errors on KNN classification. " + ex.message)
            return ClassificationData()
