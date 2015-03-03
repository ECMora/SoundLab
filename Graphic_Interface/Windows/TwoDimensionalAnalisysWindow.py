# -*- coding: utf-8 -*-
import random
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import pyqtSlot
import numpy
from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph as pg
from PyQt4 import QtGui, QtCore
from Utils.Utils import save_image
from graphic_interface.dialogs.ManualClassificationDialog import ManualClassificationDialog
from graphic_interface.windows.ui_python_files.Two_Dimensional_AnalisysWindowUI import Ui_TwoDimensionalWindow


class TwoDimensionalAnalisysWindow(QtGui.QMainWindow, Ui_TwoDimensionalWindow):
    """
    Window that provide an interface to create two dimensional
    graphs.
    """

    # region SIGNALS

    # Signal raised when an element is selected in the graph.
    # Raise the index of the selected element
    elementSelected = QtCore.Signal(int)

    # Signal raised when a selection of elements are manually classified.
    # raise the classification indexes of the elements as a list and
    # the ClassificationData for each one
    elementsClassified = QtCore.Signal(list, object)

    # endregion

    # region CONSTANTS

    # the width by default of the dock window with the options of the graph
    DOCK_WINDOW_WIDTH = 200

    # the color of the selected element brush
    SELECTED_ELEMENT_COLOR = "FFF"

    # endregion

    # region Initialize

    def __init__(self, parent, segmentManager):
        """
        Create a new window for two dimensional graphs
        :param parent: parent window if any
        :param columns: the columns of measured parameters
        :param data: Matrix of columns*number of elements.
        In data[i,j] is the medition of the parameter columns[i] in the j detected element
        :param classificationData:  the clasification data for the clasification
        :return:
        """
        super(TwoDimensionalAnalisysWindow, self).__init__(parent)
        self.setupUi(self)

        # initialization settings for the plot widget
        self.configure_widget()

        self.segmentManager = segmentManager

        # scatter plot to graphs the elements
        self.scatter_plot = None

        # font to use in the axis of the graph
        self.font = QtGui.QFont()

        # index of the element currently selected in the widget if any
        # if no selection element then -1
        self.selectedElementIndex = -1

        self.create_parameter_tree(self.segmentManager.parameterColumnNames)

        self.show()

    def configure_widget(self):
        """
        Set a group of initial configuration on the visualization widget
        :return:
        """
        self.widget.getPlotItem().showGrid(x=True, y=True)
        self.widget.getPlotItem().hideButtons()
        self.widget.setMouseEnabled(x=False, y=False)
        self.widget.setMenuEnabled(False)
        self.widget.enableAutoRange()

        self.widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.widget.addAction(self.actionHide_Show_Settings)
        self.widget.addAction(self.actionSaveGraphImage)
        self.widget.addAction(self.actionMark_Selected_Elements_As)

    def create_parameter_tree(self, parameterColumnNames):
        """
        Create the parameter tree with the visual options according to the
        measured parameters.
        :param parameterColumnNames: the names of the measured parameters
        :return:
        """
        if len(parameterColumnNames) == 0:
            return

        # the X axis posible params names
        x_axis = [unicode(x) for x in parameterColumnNames]

        # get two initial random parameters to visualize in x and y axis
        x, y = random.randint(0, len(x_axis) / 2), random.randint(len(x_axis) / 2, len(x_axis) - 1)

        # set the layout for the widget
        lay1 = QtGui.QVBoxLayout()
        lay1.setMargin(0)

        # region Set the parameter tree settings
        params = [
            {u'name': unicode(self.tr(u'X Axis Parameter Settings')), u'type': u'group', u'children':
                [{u'name': unicode(self.tr(u'X Axis')), u'type': u'list', u'value': x,
                  # the possible values to select for graph in the X axis (name,index)
                  u'default': x, u'values': [(name, i) for i, name in enumerate(x_axis)]}]},
            {u'name': unicode(self.tr(u'Y Axis Parameter Settings')), u'type': u'group', u'children':
                [{u'name': unicode(self.tr(u'Y Axis')), u'type': u'list', u'value': y,
                  # the possible values to select for graph in the Y axis (name,index)
                  u'default': y, u'values': [(name, i) for i, name in enumerate(x_axis)]}]},
            {u'name': unicode(self.tr(u'Color')), u'type': u'color', u'value': "00F"},
            {u'name': unicode(self.tr(u'Figures Size')), u'type': u'int', u'value': 15},
            {u'name': unicode(self.tr(u'Figures Shape')), u'type': u'list', u'value': "o",
             u'default': "o",
             u'values': [("Circle", "o"), ("Square", "s"), ("Triangle", "t"), ("Diamond", "d"), ("Plus", "+")]},
            {u'name': unicode(self.tr(u'Change Font')), u'type': u'action'},
            {u'name': unicode(self.tr(u'Save Graph as Image')), u'type': u'action'}]

        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)
        self.parameterTree = ParameterTree()
        lay1.addWidget(self.parameterTree)
        self.parameterTree.setAutoScroll(True)
        self.parameterTree.setHeaderHidden(True)
        self.parameterTree.setParameters(self.ParamTree, showTop=False)

        self.dockWidgetContents.setLayout(lay1)
        self.dockWidgetContents.setStyleSheet("background-color:#DDF")
        self.parameterTree.setMinimumWidth(self.DOCK_WINDOW_WIDTH)
        self.ParamTree.sigTreeStateChanged.connect(self.plot)
        self.ParamTree.param(unicode(self.tr(u'Save Graph as Image'))).sigActivated.connect(
            self.on_actionSaveGraphImage_triggered)
        self.ParamTree.param(unicode(self.tr(u'Change Font'))).sigActivated.connect(self.changeFont)

        # endregion

        # visualize the changes
        self.plot()

    # endregion

    # region Graph Managing

    def load_data(self, segment_manager):
        """
        Load a new detection data. Update the graph and the internal variables
        from the segment manager.
        :return:
        """
        self.deselect_element()

        # removes the old combo with the old measurements
        # the x axis old measurements
        self.ParamTree.param(unicode(self.tr(u'X Axis Parameter Settings'))).removeChild(
            self.ParamTree.param(unicode(self.tr(u'X Axis Parameter Settings'))).
            param(unicode(self.tr(u'X Axis'))))

        # the y axis old measurements
        self.ParamTree.param(unicode(self.tr(u'Y Axis Parameter Settings'))).removeChild(
            self.ParamTree.param(unicode(self.tr(u'Y Axis Parameter Settings'))).
            param(unicode(self.tr(u'Y Axis'))))

        # create the new combo for the new measurements
        # the x axis new measurements
        self.ParamTree.param(unicode(self.tr(u'X Axis Parameter Settings'))).addChild(
            Parameter.create(**{u'name': unicode(self.tr(u'X Axis')), u'type': u'list', u'value': 0,
                                u'default': 0, u'values':
                                [(name, i) for i, name in enumerate(segment_manager.parameterColumnNames)]}))

        # the y axis new measurements
        self.ParamTree.param(unicode(self.tr(u'Y Axis Parameter Settings'))).addChild(
            Parameter.create(**{u'name': unicode(self.tr(u'Y Axis')), u'type': u'list', u'value': 0,
                                u'default': 0, u'values':
                                [(name, i) for i, name in enumerate(segment_manager.parameterColumnNames)]}))

        self.plot()

    def update_data(self, segmentManager):
        """
        Update the data from the segment manager where a change is made
        on the amount of elements(someone(s) is(are) deleted(added)) but the parameters measured
        remains equals.
        (If the change is made on parameters must call loadData)
        :param segmentManager:
        :return:
        """
        self.segmentManager = segmentManager
        self.plot()

    def changeFont(self):
        """
        Change the font of the axis in the plot widget.
        """
        self.font, ok = QtGui.QFontDialog.getFont(self.font)
        if ok:
            self.widget.setAxisFont("bottom", self.font)
            self.widget.setAxisFont("left", self.font)

    def plot(self):
        """
        Plot the two dimensional graph with the options settings defined by user.
        :return:
        """
        self.widget.clear()

        # get the indexes of the two params X and Y for each axis values to graph
        x_axis_index = self.ParamTree.param(unicode(self.tr(u'X Axis Parameter Settings'))).param(
                                            unicode(self.tr(u'X Axis'))).value()

        y_axis_index = self.ParamTree.param(unicode(self.tr(u'Y Axis Parameter Settings'))).param(
                                            unicode(self.tr(u'Y Axis'))).value()

        # get the visual options of the graph
        color = self.ParamTree.param(unicode(self.tr(u'Color'))).value()
        shape = self.ParamTree.param(unicode(self.tr(u'Figures Shape'))).value()
        fig_size = self.ParamTree.param(unicode(self.tr(u'Figures Size'))).value()

        # get the values x,y of each element according to the measured parameter selected in each axis
        x_cords = [e[x_axis_index] for e in self.segmentManager.measuredParameters]
        y_cords = [e[y_axis_index] for e in self.segmentManager.measuredParameters]

        xmin, xmax = min(x_cords), max(x_cords)
        ymin, ymax = min(y_cords), max(y_cords)

        # space in x and y axis for center the visible elements and set the
        # visible range a little more bigger than just the area that enclose them
        xshift = (xmax - xmin) * 0.15  # 15 % for every side left and rigth
        yshift = (ymax - ymin) * 0.15  # 15 % up and down

        # create the scatter plot with the values
        self.scatter_plot = pg.ScatterPlotItem(x=x_cords, y=y_cords,
                                               data=numpy.arange(len(x_cords)),
                                               size=fig_size, symbol=shape, brush=(pg.mkBrush(color)))

        # connect the signals for selection item on the plot
        self.scatter_plot.sigClicked.connect(self.elementFigureClicked)

        elems = self.scatter_plot.points()

        # draw the selected element with a different brush
        if 0 <= self.selectedElementIndex < len(elems):
            elems[self.selectedElementIndex].setBrush(pg.mkBrush("FFF"))

        # update font size in axis labels
        text_size = {'color': '#FFF', 'font-size': str(self.font.pointSize()) + 'pt'}
        self.widget.setAxisLabel("bottom", str(self.segmentManager.parameterColumnNames[x_axis_index]), **text_size)

        self.widget.setAxisLabel("left", str(self.segmentManager.parameterColumnNames[y_axis_index]), **text_size)

        # add the plot to the widget
        self.widget.addItem(self.scatter_plot)

        # set range to the visible region of values
        self.widget.setRange(xRange=(xmin - xshift, xmax + xshift),yRange=(ymin - yshift, ymax + yshift))

        # clear the selection rectangle
        self.widget.removeSelectionRect()
        self.widget.addSelectionRect()

    # endregion

    # region Elements Selection

    def select_element(self, index):
        """
        Select the element at index 'index' in the graph.
        If index is outside of the elements count range nothing is do it.
        :param index: The index of the element to select.
        :return:
        """
        if self.scatter_plot is None or self.selectedElementIndex == index:
            return

        # get the current elements on the graph
        elems = self.scatter_plot.points()
        if not 0 <= index < len(elems):
            return

        # get the color of the not selected elements
        color = self.ParamTree.param(unicode(self.tr(u'Color'))).value()

        element_to_select = elems[index]
        element_to_select.setBrush(pg.mkBrush(self.SELECTED_ELEMENT_COLOR))

        # update the old selected element to unselected (if any)
        if self.selectedElementIndex != -1:
            elems[self.selectedElementIndex].setBrush(pg.mkBrush(color))

        # update the state variable of last selected element
        self.selectedElementIndex = index

    def deselect_element(self):
        """
        Deselect the element currently selected (if any) on the graph.
        :return:
        """
        if self.scatter_plot is None or self.selectedElementIndex < 0:
            return

        # get the color of the normal element figures on the graph
        color = self.ParamTree.param(unicode(self.tr(u'Color'))).value()

        # set the normal brush color to the element selected
        self.scatter_plot.points()[self.selectedElementIndex].setBrush(pg.mkBrush(color))

        self.selectedElementIndex = -1

    def elementFigureClicked(self, x, y):
        """
        Method that listen to the event of click an element on the scatter plot graph.
        :param x:
        :param y:
        :return:
        """
        self.select_element(y[0].data())
        self.elementSelected.emit(y[0].data())

    # endregion

    def load_workspace(self, workspace):
        """
        Update the visual theme of the window with the values from
        the application.
        :param theme: The visual theme currently used in the application.
        :return:
        """
        self.widget.setBackground(workspace.workTheme.oscillogramTheme.background_color)

        xGrid, yGrid = workspace.workTheme.oscillogramTheme.gridX, workspace.workTheme.oscillogramTheme.gridY

        self.widget.showGrid(x=xGrid, y=yGrid)

    @pyqtSlot()
    def on_actionHide_Show_Settings_triggered(self):
        """
        Switch the visibility of the settings window
        :return:
        """
        visibility = self.dockGraphsOptions.isVisible()
        self.dockGraphsOptions.setVisible(not visibility)

        if not visibility:
            # if was previously invisible
            self.dockGraphsOptions.setFloating(False)

    @pyqtSlot()
    def on_actionSaveGraphImage_triggered(self):
        """
        Save the widget graph as image
        :return:
        """
        fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save two dimensional graph as an Image"),
                                                    u"two-dim-graph-Duetto-Image",
                                                    u"*.jpg"))
        save_image(self.widget, fname)

    @pyqtSlot()
    def on_actionMark_Selected_Elements_As_triggered(self):
        """
        Make the manual classification of elements on the graph.
        @return: the indexes of the manually classified selected elements in the graph.
        """
        if self.scatter_plot is None:
            return []

        rect = self.widget.ElementSelectionRect.rect()

        # get the rect bounds
        x1, y1 = rect.x(), rect.y()
        x2, y2 = x1 + rect.width(), y1 + rect.height()

        # the width and height could be negatives
        x1, x2, y1, y2 = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)

        # get the elements that are on the range marked by the rectangle
        selected_elements = [x.data() for x in self.scatter_plot.points()
                             if x1 <= x.pos().x() <= x2 and
                             y1 <= x.pos().y() <= y2]

        if len(selected_elements) == 0:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), self.tr(u"Warning"), self.tr(u"There is no element selected."))
            return

        # get the selection
        classification_dialog = ManualClassificationDialog()
        classification_dialog.exec_()

        self.elementsClassified.emit(selected_elements, classification_dialog.get_classification())