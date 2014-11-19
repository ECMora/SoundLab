from duetto.widgets.OscillogramWidget import OscillogramWidget
from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.RectangularCursorTool import RectangularCursorTool
from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.ZoomTool import ZoomTool

from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.PointerCursorTool import PointerCursorTool


class SoundLabOscilogramWidget(OscillogramWidget):

    def __init__(self):
        OscillogramWidget.__init__(self)
        self.gui__user_tool = None
        self.changeTool(ZoomTool)
        # #probando cambio de herramientas
        # self.tools = [RectangularCursorTool, ZoomTool, PointerCursorTool]
        # self.index = 0

    # def c(self):
    #     self.changeTool(self.tools[self.index])
    #     self.index = (self.index + 1)% 3

    def mouseMoveEvent(self, event):
        self.gui__user_tool.mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.gui__user_tool.mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.gui__user_tool.mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        self.gui__user_tool.mouseReleaseEvent(event)

    def changeTool(self, new_tool_class):
        if new_tool_class is None:
            raise Exception("The user visual tool can't be None")
        #check that new tool is descendant of Tools
        if self.gui__user_tool is not None:
            self.gui__user_tool.dispose()
        self.gui__user_tool = new_tool_class(self)
        self.gui__user_tool.detectedDataChanged.connect(self.printData)

    def printData(self,d):
        s = " "
        for atr_name,value in d:
            s += str(atr_name) + ": " +str(value) + " "
        print(s)

    def zoom(self, indexFrom=0, indexTo=-1):
        pass