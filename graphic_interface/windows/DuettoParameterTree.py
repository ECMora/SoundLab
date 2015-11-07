from PyQt4 import QtGui
from pyqtgraph.parametertree import ParameterTree, registerParameterType, Parameter
from pyqtgraph.parametertree.parameterTypes import WidgetParameterItem, SimpleParameter


class DuettoParameterTree(ParameterTree):
    """
    Extension of parameter tree widget of pyqtgraph to change visual
    options for the system.
    """

    # the amount of pixels used for children parameter tree delimitation
    APP_PARAMETER_TREE_INDENTATION = 10

    def __init__(self, *args,**kwargs):
        ParameterTree.__init__(self, *args, **kwargs)

        self.setIndentation(self.APP_PARAMETER_TREE_INDENTATION)


class DuettoWidgetParameterItem(WidgetParameterItem):
    """
    Redefine the widget to use in parameter trees to controle
    it layouts
    """

    def __init__(self, param, depth):
        WidgetParameterItem.__init__(self, param, depth)

        self.displayLabel = QtGui.QLabel()

        # redefine the layout for default button
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.addWidget(self.widget)
        layout.addWidget(self.displayLabel)
        # layout.addWidget(self.defaultBtn)
        self.layoutWidget = QtGui.QWidget()
        self.layoutWidget.setLayout(layout)

