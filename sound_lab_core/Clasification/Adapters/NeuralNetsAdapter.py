import os
import pickle
from pyqtgraph.parametertree import Parameter
from sound_lab_core.Clasification.Adapters.ClassifierAdapter import ClassifierAdapter
from sound_lab_core.Clasification.Classifiers import NeuralNet
from sound_lab_core.Clasification.Classifiers.NeuralNetsClassifier import NeuralNetsClassifier


# check classifiers params property
class NeuralNetsAdapter(ClassifierAdapter):
    """
    Adapter class for the Neural Net classifier
    """

    NNdir = "./sound_lab_core/Clasification/Classifiers/Neural Nets/"
    NETWORKS = ['family', 'specie', 'genus']

    def __init__(self):

        ClassifierAdapter.__init__(self)
        # Context available classifiers
        self. _classifiers = {}

        self.name = u'Neural Nets'

        # get available context trained networks
        for context in self.NETWORKS:

            # load pre trained context neural nets
            try:
                self._classifiers[context] = self._load(self.NNdir + "/" + context + '.net')
            except Exception:
                self._classifiers[context] = None

        if len(self._classifiers) == 0:
            return

        list = []
        for context in self.NETWORKS:
            classifier = self._classifiers[context]
            if classifier is not None:
                for param in classifier.params:
                    if param not in list:
                        list.append(param)
        self._params = list

        family = self._classifiers['family'] is not None
        genus = self._classifiers['genus'] is not None
        specie = self._classifiers['specie'] is not None

        settings = [{u'name': u'Family', u'type': u'bool', 'enabled': family ,u'default': family,
                    u'value':family},
                    {u'name': u'Genus', u'type': u'bool', 'enabled': genus ,u'default': genus,
                     u'value':genus},
                    {u'name': u'Specie', u'type': u'bool', 'enabled': specie ,u'default': specie,
                    u'value':specie},
                    {'name': u'Information', 'type': 'text', 'value': unicode(self.get_classifiers_info())},
                    {'name': u'More', 'type': 'action'}]

        self.settings = Parameter.create(name=u'Settings', type=u'group', children=settings)
        # self.settings.sigStateChanged.connect(self.neuralNetsParamChanged)

    def _load(self, filename):
        if not os.path.exists(filename):
            raise Exception('File does not exist.')

        with open(filename, 'rb') as f:
            return pickle.load(f)

    def get_classifiers_info(self):
        info = ""

    def classifier_parameters(self):
        return self._params

    def get_settings(self):
        return self.settings

    def get_instance(self):

        # check user context classes selected for classification
        family = self._classifiers['family'] if self.settings.param('Family').value() else None
        genus = self._classifiers['genus'] if self.settings.param('Genus').value() else None
        specie = self._classifiers['specie'] if self.settings.param('Specie').value() else None

        return NeuralNetsClassifier(self._params, familyNet=family, genusNet=genus, specieNet=specie)