from pyqtgraph.parametertree import Parameter
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class LocationAdapter(SoundLabAdapter):
    """
    An adapter base class to create locations for parameter measurements
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

        self.settings = Parameter.create(name=u'Time Location', type=u'group', children=[])

    def get_instance(self):
        """
        The location adapter returns a list with all the locations
        that the adapter is managing. A single adapter could manage
        multiple locations of a same type. Example: Segment x-distant
        divided by n then return n locations
        :return:
        """
        return []

    def get_settings(self):
        """
        returns a Parameter Tree with the options of the abs decay detector
        """
        return self.settings