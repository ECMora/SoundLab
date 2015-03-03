# -*- coding: utf-8 -*-
from Utils.db.DB_ORM import get_db_session, Parameter
from sound_lab_core.ParametersMeasurement.Adapters.ParameterAdapter import ParameterAdapter
from sound_lab_core.ParametersMeasurement.TimeParameters.DurationTimeParameter import DurationTimeParameter


class DurationTimeParameterAdapter(ParameterAdapter):
    """
    Adapter class for the start time parameter.
    """

    def __init__(self):
        ParameterAdapter.__init__(self)

    def _get_orm_mapper(self):
        # get the db object mapper
        try:
            db_session = get_db_session()
            parameters_list = db_session.query(Parameter).filter(Parameter.name == "Duration(s)").all()
            if db_session:
                self.db_mapper = parameters_list[0]
            print(self.db_mapper)
        except Exception as ex:
            print("db connection error. " + ex.message)
            pass

    def get_instance(self):
        return DurationTimeParameter()




