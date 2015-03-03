from Utils.db.DB_ORM import get_db_session, Parameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class ParameterAdapter(SoundLabAdapter):

    def __init__(self):
        SoundLabAdapter.__init__(self)

    def get_db_orm_mapper(self):
        if self.db_mapper is None:
            self.db_mapper = self._get_db_orm_mapper()
        return self.db_mapper

    def _get_db_orm_mapper(self):
        """
        Method that connects to the db to search the current adapter
        object db orm representation if any
        :return:
        """
        # get the db object mapper

        try:
            db_session = get_db_session()
            parameter_name = self.get_instance().name
            parameters_list = db_session.query(Parameter).filter(Parameter.name == parameter_name).all()
            if db_session:
                self.db_mapper = parameters_list[0]

        except Exception as ex:
            print("db connection error. " + ex.message)
            self.db_mapper = None

        return self.db_mapper