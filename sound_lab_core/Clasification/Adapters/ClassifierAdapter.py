from graphic_interface.segment_visualzation.classification_items.ClassificationVisualItem import ClassificationVisualItem
from sound_lab_core.SoundLabAdapter import SoundLabAdapter


class ClassifierAdapter(SoundLabAdapter):
    """
    Adapter class for the manual classifier
    """

    def __init__(self):
        SoundLabAdapter.__init__(self)

    def get_visual_item(self):
        """
        The instance of the visual item to include in the visual widgets
        to visualize the segment Classification (if any)
        :return:
        """
        return ClassificationVisualItem()
