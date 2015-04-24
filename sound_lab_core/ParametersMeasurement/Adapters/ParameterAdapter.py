from utils.db.DB_ORM import DB, Parameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class ParameterAdapter(SoundLabAdapter):
    """
    The base of implementations for parameters
    measurements.
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

    def get_db_orm_mapper(self):
        """
        Get the db orm instance class for the current parameter
        :return:
        """
        if self.db_mapper is None:
            self.db_mapper = self._get_db_orm_mapper()
        return self.db_mapper

    def _get_db_orm_mapper(self):
        """
        Method that connects to the db to search the current adapter
        object db orm representation if any
        :return:
        """
        # get the db object mapper for the parameter
        try:
            db_session = DB().get_db_session()
            # find by name
            parameter_name = self.get_instance().name
            for param in db_session.query(Parameter).filter(Parameter.name == parameter_name).all():
                return param

        except Exception as ex:
            print("db connection error. Parameter" + ex.message)
            return None