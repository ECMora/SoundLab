# -*- coding: utf-8 -*-

Zoom,RectangularCursor,CircularEraser,RectangularEraser,PointerCursor, OscilogramThreshold = range(6)

class SignalVisualizerTool:
    """
    Base class for the tools used in the QSignalVisualizerWidget.
    Encapsulates method for user interaction with the visual controls.
    All the signal_visualizer_tools must manage the gui events
    corresponding to its function
    """
    pass

