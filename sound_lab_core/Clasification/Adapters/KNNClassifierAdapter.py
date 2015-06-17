# -*- coding: utf-8 -*-
from pyqtgraph.parametertree import Parameter
from sqlalchemy import or_
from sound_lab_core.Clasification.Adapters.ClassifierAdapter import ClassifierAdapter
from sound_lab_core.Clasification.Classifiers.KNNClassifier import KNNClassifier
from sound_lab_core.ParametersMeasurement.Adapters import DurationTimeParameterAdapter
from utils.db.DB_ORM import Segment, DB


class KNNClassifierAdapter(ClassifierAdapter):
    """
    Adapter class for the manual classifier
    """

    def __init__(self):
        ClassifierAdapter.__init__(self)
        db_session = DB().get_db_session()

        self.name = u'KNN'

        training_vector_count = db_session.query(Segment).filter(or_(Segment.specie != None,
                                                                     Segment.genus != None,
                                                                     Segment.family != None)).count()

        if training_vector_count <= 10:
            # from 10 to 50 steps of 5
            start, stop, step, selected = 1, training_vector_count, 1, min(training_vector_count, 10)

        elif training_vector_count < 100:
            # from 10 to 50 steps of 5
            start, stop, step, selected = 10, min(training_vector_count, 50), 5, 10

        elif training_vector_count < 1000:
            # from 50 to 300 steps of 10
            start, stop, step, selected = 50, min(training_vector_count, 300), 10, 50

        else:
            # from 200 to 500 steps of 20
            start, stop, step, selected = 200, min(training_vector_count, 500), 20, 200

        k_list = [(unicode(x), x) for x in xrange(start, stop, step)]
        settings = [{u'name': unicode(self.tr(u'K-Value')), u'type': u'list', u'default': selected,
                     u'values': k_list,
                     u'value': unicode(selected)}]

        self.k_value = selected

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)

    def classifier_parameters(self):
        """
        The list of the measured parameters needed to the specified classifier
        :return:
        """
        return [DurationTimeParameterAdapter()]

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings

    def get_instance(self):
        """
        Gets a new get_instance
        """
        try:
            k_value = self.settings.param(unicode(self.tr(u'K-Value'))).value()

        except Exception as ex:
            k_value = 10

        self.k_value = k_value

        return KNNClassifier(self.k_value)

    def restore_settings(self, adapter_copy, signal):
        if not isinstance(adapter_copy, ClassifierAdapter) or \
                not isinstance(adapter_copy, KNNClassifierAdapter):
            raise Exception("Invalid type exception.")

        # get the settings from the copy
        adapter_copy.get_instance()
        self.settings.param(unicode(self.tr(u'K-Value'))).setValue(adapter_copy.k_value)