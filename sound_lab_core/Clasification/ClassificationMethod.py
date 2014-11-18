from sound_lab_core.Clasification import ClassificationData


class ClassificationMethod:
    def __init__(self, classificationData=None):
        if not isinstance(classificationData, ClassificationData):
            raise TypeError("classificationData is not of type ClassificationData")
        self.data = classificationData

    def classify(self,vector):
        pass
