class Element:
    """
    Represents the minimal piece of information to clasify
    An element in an N dimensional transform of the signal. Is an N dimensional region
    that contains a superior energy that the fragment of signal near to it.
    Ej of 1 dimensional Transform : scale, normalize, oscilogram
    Ej of 2 dimensional Transform : spectrogram
    """
    def __init__(self, signal):
        #the signal in wich this elements is defined
        self.signal=signal
        #the optional data interesting for the transform ej name, parameters, etc
        self.visible = True #visual opions for ploting
        self.visualwidgets =[] #the objects to represent visually this object
