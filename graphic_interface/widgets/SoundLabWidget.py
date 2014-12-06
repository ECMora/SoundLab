from signal_visualizer_tools.SignalVisualizerTool import SignalVisualizerTool


class SoundLabWidget:

    def __init__(self):
        self.gui_user_tool = None
        self.theme = None

    def mouseMoveEvent(self, event):
        if self.gui_user_tool is not None:
            self.gui_user_tool.mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if self.gui_user_tool is not None:
            self.gui_user_tool.mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.gui_user_tool is not None:
            self.gui_user_tool.mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        if self.gui_user_tool is not None:
            self.gui_user_tool.mouseReleaseEvent(event)

    def changeTool(self, new_tool_class):
        if new_tool_class is None:
            raise Exception("The user visual tool can't be None")
        # check that new tool is descendant of Tools
        if not issubclass(new_tool_class, SignalVisualizerTool):
            raise Exception("The tool must be of type SignalVisualizerTool")

        if self.gui_user_tool is not None:
            #remove old data and release resources from the tool operation
            self.gui_user_tool.dispose()
        self.gui_user_tool = new_tool_class(self)
        self.gui_user_tool.detectedDataChanged.connect(self.guiToolDetectedData)

    def guiToolDetectedData(self,data_list):
        s = " "
        for atr_name,value in data_list:
            s += str(atr_name) + ": " + str(value) + " "
        self.toolDataDetected.emit(s)

    def load_Theme(self, theme):
        """
        Loads a visual theme and applies changes. Repaints the widget if necessary.
        :param theme: an instance of the theme class for this widget, the theme to load
        """
        pass

