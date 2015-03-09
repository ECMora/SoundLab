from sqlalchemy import or_, and_
from sound_lab_core.Clasification.ClassificationData import ClassificationData
from sound_lab_core.Clasification.Classifier import Classifier
from utils.db.DB_ORM import Segment, DB, Measurement


class TrainingVector:
    """
    A vector to use for training and classification.
    Is an array of values form parameter measurements
    and the identification object (taxonomic classification)
    """

    def __init__(self, values, identification=None):
        # the classification data for the training vector
        self.identification = identification if identification is not None else ClassificationData()

        # the list of parameter values (float numbers)
        self.values = values


class TrainingVectorClassifier(Classifier):
    """
    Represents the base class for the classifiers that
    uses training vectors
    """

    def __init__(self, name=""):
        Classifier.__init__(self, name)

        # the current training vectors list to make classification
        # each element on list is a Training Vector measured.
        self.training_vectors = None

        # the list of parameter adapters that would be used in classification
        self._parameters = []

        # the session to request the db for training vectors
        self.db_session = DB().get_db_session()

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameter_measurements_list):
        """
        Set the list of parameter adapters used.
        :param parameter_measurements_list:
        :return:
        """
        # order parameters by db id to normalize their use
        params_ids = [x.get_db_orm_mapper().parameter_id for x in parameter_measurements_list]
        params_to_sort = [(parameter_measurements_list[i], params_ids[i]) for i in xrange(len(params_ids))]
        params_to_sort.sort(lambda x, y: 1 if x[1] < y[1] else 1)

        self._parameters = [x[0] for x in params_to_sort]
        self.training_vectors = self.get_training_vectors()

    def get_training_vectors(self):
        """
        load from db the training vectors according to the parameter adapters list
        :return:
        """
        if len(self.parameters) == 0:
            return []

        vectors = []
        try:
            parameter_ids = set(map(lambda param: param.get_db_orm_mapper().parameter_id, self.parameters))

            # get the db parameter values for the parameters list
            for x in self.db_session.query(Segment).\
                    filter(or_(Segment.specie != None, Segment.genus != None,
                               Segment.family != None)).all():

                parameter_measurement_ids = set(map(lambda x: x.parameter_id, x.measurements))

                if parameter_ids.issubset(parameter_measurement_ids):
                    x.measurements.sort(lambda x, y: -1 if x.parameter_id < y.parameter_id else 1)

                    measurements = x.measurements[:len(parameter_ids)]

                    values = [self.db_session.query(Measurement).\
                                              filter(and_(Measurement.segment_id == x.segment_id,
                                                          Measurement.parameter_id == p.parameter_id)).all()[0].value
                              for p in measurements]

                    identification = ClassificationData(specie=x.specie, genus=x.genus, family=x.family)
                    vectors.append(TrainingVector(values, identification))

        except Exception as ex:
            print("Error searching the training vectors on db. " + ex.message)
            vectors = []

        return vectors



