from pyqtgraph.parametertree.parameterTypes import WidgetParameterItem
from pyqtgraph.python2_3 import asUnicode
from PyQt4 import QtCore, QtGui


class DuettoListParameterItem(WidgetParameterItem):
    """
    WidgetParameterItem subclass providing comboBox that lets the user select from a list of options.

    """
    def __init__(self, param, depth):
        param.opts[u'value'] = param.opts[u'default']
        self.targetValue = None
        self.values = param.opts.get(u'values',[])
        self.valuesDict = {}
        for (a, b) in self.values:
            self.valuesDict[a] = b
        WidgetParameterItem.__init__(self, param, depth)
        self.widget.sigChanged.connect(self.widgetValueChanged)


    def makeWidget(self):
        opts = self.param.opts
        t = opts[u'type']
        w = QtGui.QComboBox()
        w.setMaximumHeight(20)  ## set to match height of spin box and line edit
        w.sigChanged = w.currentIndexChanged
        w.value = self.value
        w.setValue = self.setValue
        self.widget = w  ## needs to be set before limits are changed
        self.limitsChanged(self.param, self.param.opts['limits'])
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
