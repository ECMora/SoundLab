from graphic_interface.segment_visualization.classification_items.ClassificationVisualItem import ClassificationVisualItem
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class ClassifierAdapter(SoundLabAdapter):
    """
    Adapter class for the manual classifier
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

