class Element:
    """
    Represents the minimal piece of information to clasify
    An element in an N dimensional transform of the signal. Is an N dimensional region
    that contains a superior energy that the fragment of signal near to it.
    Ej of 1 dimensional Transform : scale, normalize, oscilogram
    Ej of 2 dimensional Transform : spectrogram
    """
    Locations,Figures,Text,PeakFreqs=range(4)
    def __init__(self, signal):
        #the signal in wich this elements is defined
        self.signal = signal
        #the optional data interesting for the transform ej name, parameters, etc
        self.visible = True #visual opions for ploting
        self.visual_text = []
        self.visual_locations = []
        self.visual_figures = []
        self.visual_peaksfreqs = []



    def visualwidgets(self):
        for t in self.visual_text:
            yield t
        for l in self.visual_locations:
            yield l
        for f in self.visual_figures:
            yield f
        for p in self.visual_peaksfreqs:
            yield p
        #the objects to represent visually this object
