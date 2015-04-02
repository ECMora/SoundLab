from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class ClassifierAdapter(SoundLabAdapter):
    """
    Adapter class for the manual classifier
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

    def classifier_parameters(self):
        """
        The list of the measured parameters needed to the specified classifier
        :return:
        """
        return []