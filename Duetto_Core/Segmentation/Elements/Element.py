# -*- coding: utf-8 -*-
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
        self.visible = True #visual opions for ploting the element
        self.visual_text = []  #the visual elements that show text
        self.visual_locations = []  #the visual elements that show the location of measurement (unused)
        self.visual_figures = []  #the visual elements that show the elements figures
        self.visual_peaksfreqs = []
        self.actionVisibility = None #accion que cambia la visibilidad de este elemento en el grafico para ponerla en un context menu



    def visualwidgets(self):
        """
        all the visual elements has the form (object element,bool visible)
        @return:
        """
        for f in self.visual_figures:
            yield f
        for l in self.visual_locations:
            yield l
        for t in self.visual_text:
            yield t
        for p in self.visual_peaksfreqs:
            yield p
        #the objects to represent visually this object


