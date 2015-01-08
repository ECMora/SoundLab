from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.ZoomTool import ZoomTool
from graphic_interface.widgets.signal_visualizer_tools.SpectrogramTools.SpectrogramZoomTool import SpectrogramZoomTool
from signal_visualizer_tools.SignalVisualizerTool import SignalVisualizerTool


class SoundLabWidget:
    """

    """

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

    def leaveEvent(self, QEvent):
        # avoid the zoom tool to be disabled in just one widget
        if self.gui_user_tool is not None and \
           not isinstance(self.gui_user_tool,(ZoomTool,SpectrogramZoomTool)):
            self.gui_user_tool.disable()

    def enterEvent(self, QEvent):
        # avoid the zoom tool to be disabled in just one widget
        if self.gui_user_tool is not None:
            self.gui_user_tool.enable()

    def changeTool(self, new_tool_class):
        if new_tool_class is None:
            raise Exception("The user visual tool can't be None")

        # check that new tool is descendant of Tools
        if not issubclass(new_tool_class, SignalVisualizerTool):
            raise Exception("The tool must be of type SignalVisualizerTool")

        if self.gui_user_tool is not None:
            # remove old data and release resources from the tool operation
            self.gui_user_tool.disable()

        self.gui_user_tool = new_tool_class(self)
        self.gui_user_tool.enable()
        self.gui_user_tool.detectedDataChanged.connect(self.guiToolDetectedData)

    def guiToolDetectedData(self, data_list):
        s = " "
        decimal_places = self.gui_user_tool.DECIMAL_PLACES

        for atr_name,value in data_list:
            value_str = str(value)
            # str to concat at front of values strings to make const the amount of
            # chars used on each value
            # 1 char for sign (- or ' ') 3 for numbers
            negative_padd = " " if value >= 0 else ""
            negative_padd += "" if abs(value) >= 100 else (" " if abs(value) >= 10 else "  ")
            try:
                decimals = value_str[value_str.rindex("."):]
                # concat as much '0' to the end of the str as chars to complete the decimal places
                # + 1 because decimals contains the '.' too
                value_str += "0" * (decimal_places - len(decimals) + 1)

            except Exception as ex:
                pass

            s += str(atr_name) + ": " + negative_padd + value_str + " "
        self.toolDataDetected.emit(s)

    def load_Theme(self, theme):
        """
        Loads a visual theme and applies changes. Repaints the widget if necessary.
        :param theme: an instance of the theme class for this widget, the theme to load
        """
        pass
