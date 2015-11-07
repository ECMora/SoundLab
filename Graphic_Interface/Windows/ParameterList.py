from pyqtgraph.parametertree import Parameter
from pyqtgraph.parametertree.parameterTypes import WidgetParameterItem
from pyqtgraph.python2_3 import asUnicode
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg


class DuettoListParameterItem(WidgetParameterItem):
    """
    WidgetParameterItem subclass providing comboBox that lets the user select from a list of options.

    """
    def __init__(self, param, depth):
        param.opts[u'value'] = param.opts[u'default']
        self.targetValue = None
        self.values = param.opts.get(u'values', [])
        self.valuesDict = {}

        for (a, b) in self.values:
            self.valuesDict[a] = b

        WidgetParameterItem.__init__(self, param, depth)
        self.widget.sigChanged.connect(self.widgetValueChanged)

    def makeWidget(self):
        opts = self.param.opts
        t = opts[u'type']
        w = QtGui.QComboBox()
        w.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        w.setMaximumHeight(20)  ## set to match height of spin box and line edit
        w.sigChanged = w.currentIndexChanged
        w.value = self.value
        w.setValue = self.setValue
        self.widget = w
        limits = [] if 'limits' not in self.param.opts else self.param.opts['limits']
        self.limitsChanged(self.param, limits)

        if len(self.values) > 0:
            self.setValue(self.param.value())

        return w

    def value(self):
        key = asUnicode(self.widget.currentText())
        return self.valuesDict.get(key, None)

    def setValue(self, val):
        self.targetValue = val
        if val not in self.valuesDict.values():
            self.widget.setCurrentIndex(0)
        else:
            for i in range(len(self.values)):
                if self.values[i][1] == val:
                    self.widget.setCurrentIndex(i)
                    break

    def limitsChanged(self, param, limits):
        # set up forward / reverse mappings for name:value

        if len(limits) == 0:
            limits = ['']  ## Can never have an empty list--there is always at least a singhe blank item.

        try:
            self.widget.blockSignals(True)
            val = self.targetValue  #asUnicode(self.widget.currentText())

            self.widget.clear()
            for (k,v) in self.values:
                self.widget.addItem(k)
                if v == val:
                    self.widget.setCurrentIndex(self.widget.count()-1)
                    self.updateDisplayLabel()
        finally:
            self.widget.blockSignals(False)


class DuettoListParameter(Parameter):
    itemClass = DuettoListParameterItem

    def __init__(self, *args, **kargs):
        Parameter.__init__(self, *args, **kargs)

        if self.opts['type'] == 'color':
            self.value = self.colorValue
            self.saveState = self.saveColorState

    def colorValue(self):
        return pg.mkColor(Parameter.value(self))

    def saveColorState(self):
        state = Parameter.saveState(self)
        state['value'] = pg.colorTuple(self.value())
        return state