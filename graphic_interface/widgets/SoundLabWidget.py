from graphic_interface.widgets.signal_visualizer_tools.OscilogramTools.ZoomTool import ZoomTool
from graphic_interface.widgets.signal_visualizer_tools.SpectrogramTools.SpectrogramZoomTool import SpectrogramZoomTool
from signal_visualizer_tools.SignalVisualizerTool import SignalVisualizerTool


class SoundLabWidget:
    """
    Widget that encapsulate the logic of a sound lab widget.
    Provide user interaction through mouse events to the different tools
    used on the system.
    Is defined to use as an abstract class.
    Each sound lab widget implementation is divided into the logic and the
    gui interaction. the gui interaction is made by a graphic tool and the current class
    handle it. Provide a way to change the tool and react to the gui events
    """

    def __init__(self):
        # the gui tool that is used on the widget gui interaction
        self.gui_user_tool = None

        # factorization variable for the widgets of the system that
        # all load an application theme TODO check changes with the use of the workspace
        self.theme = None

    # region Events Handling

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

    # endregion

    def changeTool(self, new_tool_class):
        """
        Change the current selected widget tool.
        :param new_tool_class: The class of the new tool
        :return:
        """
        if new_tool_class is None:
            raise Exception("The user visual tool can't be None")

        # check that new tool is descendant of Tools
        if not issubclass(new_tool_class, SignalVisualizerTool):
            raise Exception("The tool must be of type SignalVisualizerTool")

        if self.gui_user_tool is not None:
            # remove old data and release resources from the old tool operations
            self.gui_user_tool.disable()

        self.gui_user_tool = new_tool_class(self)
        self.gui_user_tool.enable()
        self.gui_user_tool.detectedDataChanged.connect(self.guiToolDetectedData)

    def guiToolDetectedData(self, data_list):
        """
        Translate the tool detected data into a string.
        :param data_list: the tool detected data
        :return: string with the detected data information
        """
        detected_data = " "
        decimal_places = self.gui_user_tool.DECIMAL_PLACES

        for atr_name,value in data_list:
            value_str = str(value)
            # str to concat at front of values strings to make const the amount of
            # chars used on each value
            # 1 char for sign (- or ' ') 3 for numbers
            negative_padd = " " if value >= -1**(-decimal_places) else ""
            negative_padd += "" if abs(value) >= 100 else (" " if abs(value) >= 10 else "  ")
            try:
                decimals = value_str[value_str.rindex("."):]
                # concat as much '0' to the end of the str as chars to complete the decimal places
                # + 1 because decimals contains the '.' too
                value_str += "0" * (decimal_places - len(decimals) + 1)

            except Exception as ex:
                pass

            detected_data += str(atr_name) + ": " + negative_padd + value_str + " "

        # raise the detected data as signal
        # the definition of the signal must be in every descendant widget
        # (python issues to solve)
        self.toolDataDetected.emit(detected_data)

    def load_Theme(self, theme):
        """
        Loads a visual theme and applies changes. Repaints the widget if necessary.
        :param theme: an instance of the theme class for this widget, the theme to load
        """
        pass
