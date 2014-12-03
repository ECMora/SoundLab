# -*- coding: utf-8 -*-
from PyQt4.QtGui import QFileDialog, QWidget
from PyQt4.QtCore import pyqtSlot
import numpy,random
from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph as pg
from Graphic_Interface.Dialogs.EditCategoriesDialog import EditCategoriesDialog
import Graphic_Interface.Dialogs.EditCategoriesDialogUI as editCateg
from Graphic_Interface.Widgets.EditCategoriesWidget import EditCategoriesWidget
from Graphic_Interface.Windows.Two_Dimensional_AnalisysWindowUI import Ui_TwoDimensionalWindow
from PyQt4 import QtGui, QtCore


class TwoDimensionalAnalisysWindow(QtGui.QMainWindow, Ui_TwoDimensionalWindow):
    """
    Window that provide an interface to create two dimensional
    graphs.
    """

    #SIGNALS
    #Signal raised when an element is selected in the graph.
    #Raise the index of the selected element
    elementSelected = QtCore.Signal(int)

    #SIGNALS
    #Signal raised when a selection of elements are manually classified.
    #raise the classification indexes of the elements as a list and the dict of Category,value for each one
    elementsClasification = QtCore.Signal(list,dict)

    def __init__(self,parent=None,columns=None, data=None, classificationData=None):
        super(TwoDimensionalAnalisysWindow, self).__init__(parent)
        self.setupUi(self)

        self.show()
        #initialization settings for the plot widget
        self.widget.getPlotItem().showGrid(x=True, y=True)
        self.widget.getPlotItem().hideButtons()
        self.widget.setMouseEnabled(x=False, y=False)
        self.widget.setMenuEnabled(False)
        self.widget.enableAutoRange()

        #scatter plot to graphs the elements
        self.scatter_plot = None

        #font to use in the axis of the graph
        self.font = QtGui.QFont()
        if classificationData is None:
            raise Exception(unicode(self.tr(u"ClassificationData could not be None.")))

        self.classificationData = classificationData
        self.previousSelectedElement = -1
        self.columns = columns if columns is not None else []

        #the numpy [,] array with the parameter measurement
        self.data = data if data is not None else numpy.zeros(4).reshape((2, 2))
        self.widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.widget.add(self.actionHide_Show_Settings)
        self.widget.add(self.actionSaveGraphImage)
        self.widget.add(self.actionMark_Selected_Elements_As)
        self.createParameterTreeOptions(self.columns)

    @pyqtSlot()
    def on_actionHide_Show_Settings_triggered(self):
        if self.dockGraphsOptions.isVisible():
            self.dockGraphsOptions.setVisible(False)
        else:
            self.dockGraphsOptions.setVisible(True)
            self.dockGraphsOptions.setFloating(False)

    def createParameterTreeOptions(self,columnNames):
        xaxis = [unicode(x) for x in columnNames]
        if len(xaxis) == 0:
            return
        x, y = random.randint(0,len(xaxis)/2),random.randint(len(xaxis)/2,len(xaxis)-1)
        params = [
            {u'name': unicode(self.tr(u'X Axis Parameter Settings')), u'type': u'group', u'children':
                [{u'name': unicode(self.tr(u'X Axis')), u'type': u'list',u'value': x,
                  u'default': x, u'values': [(name, i) for i,name in enumerate(xaxis)]}]},
            {u'name': unicode(self.tr(u'Y Axis Parameter Settings')), u'type': u'group', u'children':
                [{u'name': unicode(self.tr(u'Y Axis')), u'type': u'list', u'value':y,
             u'default': y, u'values': [(name, i) for i,name in enumerate(xaxis)]}]},
            {u'name': unicode(self.tr(u'Color')), u'type': u'color', u'value': "00F"},
            {u'name': unicode(self.tr(u'Figures Size')), u'type': u'int', u'value': 15},
            {u'name': unicode(self.tr(u'Figures Shape')), u'type': u'list', u'value': "o",
             u'default': "o", u'values': [("Circle","o"),("Square","s"),("Triangle","t"),("Diamond","d"),("Plus","+")]},
            {u'name': unicode(self.tr(u'Change Font')), u'type': u'action'},
            {u'name': unicode(self.tr(u'Save Graph as Image')), u'type': u'action'}]

        lay1 = QtGui.QVBoxLayout()
        lay1.setMargin(0)

        self.ParamTree = Parameter.create(name=u'params', type=u'group', children=params)
        self.parameterTree = ParameterTree()
        lay1.addWidget(self.parameterTree)
        self.parameterTree.setAutoScroll(True)
        self.parameterTree.setHeaderHidden(True)
        self.parameterTree.setParameters(self.ParamTree, showTop=False)
        self.dockWidgetContents.setLayout(lay1)
        self.dockWidgetContents.setStyleSheet("background-color:#DDF")
        self.parameterTree.setMinimumWidth(200)
        self.ParamTree.sigTreeStateChanged.connect(self.plot)
        self.ParamTree.param(unicode(self.tr(u'Save Graph as Image'))).sigActivated.connect(self.on_actionSaveGraphImage_triggered)
        self.ParamTree.param(unicode(self.tr(u'Change Font'))).sigActivated.connect(self.changeFont)
        self.plot()

    def loadData(self, columns=None, data=None):
        self.deselectElement()
        self.data = data
        #update graph and paramtree
        if self.columns != columns:
            xaxis = [unicode(x) for x in columns]
            self.ParamTree.param(unicode(self.tr(u'X Axis Parameter Settings'))).removeChild(self.ParamTree.param(unicode(self.tr(u'X Axis Parameter Settings'))).param(unicode(self.tr(u'X Axis'))))
            self.ParamTree.param(unicode(self.tr(u'X Axis Parameter Settings'))).addChild(Parameter.create(**{u'name': unicode(self.tr(u'X Axis')), u'type': u'list',u'value': 0,
                  u'default': 0, u'values': [(name, i) for i,name in enumerate(xaxis)]}))
            self.ParamTree.param(unicode(self.tr(u'Y Axis Parameter Settings'))).removeChild(self.ParamTree.param(unicode(self.tr(u'Y Axis Parameter Settings'))).param(unicode(self.tr(u'Y Axis'))))
            self.ParamTree.param(unicode(self.tr(u'Y Axis Parameter Settings'))).addChild(Parameter.create(**{u'name': unicode(self.tr(u'Y Axis')), u'type': u'list',u'value': 0,
                  u'default': 0, u'values': [(name, i) for i,name in enumerate(xaxis)]}))
            self.columns = columns
        self.plot()

    def changeFont(self):
        """
        Change the font of the axis in the plot widget.
        """
        self.font, ok = QtGui.QFontDialog.getFont(self.font)
        if ok:
            self.widget.getPlotItem().getAxis("bottom").setTickFont(self.font)
            self.widget.getPlotItem().getAxis("left").setTickFont(self.font)

    def load_Theme(self, theme):
        self.widget.setBackground(theme.osc_background)
        self.widget.getPlotItem().showGrid(x=theme.osc_GridX, y=theme.osc_GridY)

    def selectElement(self,index):
        if self.scatter_plot is None or self.previousSelectedElement == index:
            return
        elems = self.scatter_plot.points()
        if len(elems) <= index:
            return

        color = self.ParamTree.param(unicode(self.tr(u'Color'))).value()
        elem = elems[index]
        elem.setBrush(pg.mkBrush("FFF"))
        if self.previousSelectedElement != -1:
            elems[self.previousSelectedElement].setBrush(pg.mkBrush(color))

        self.previousSelectedElement = index

    def deselectElement(self):
        if self.scatter_plot is None or self.previousSelectedElement < 0 :
            return
        color = self.ParamTree.param(unicode(self.tr(u'Color'))).value()

        self.scatter_plot.points()[self.previousSelectedElement].setBrush(pg.mkBrush(color))

    @pyqtSlot()
    def on_actionSaveGraphImage_triggered(self):
        fname = unicode(QFileDialog.getSaveFileName(self, self.tr(u"Save two dimensional graphics as an Image "),self.tr(u"-Duetto-Image"),"*.jpg"))
        if fname:
            #save as image
            image = QtGui.QPixmap.grabWindow(self.widget.winId())
            image.save(fname, 'jpg')

    def plot(self):
        #the elements and the colors to plot
        self.widget.clear()

        i, j = self.ParamTree.param(unicode(self.tr(u'X Axis Parameter Settings'))).param(unicode(self.tr(u'X Axis'))).value(),\
               self.ParamTree.param(unicode(self.tr(u'Y Axis Parameter Settings'))).param(unicode(self.tr(u'Y Axis'))).value()

        color = self.ParamTree.param(unicode(self.tr(u'Color'))).value()
        shape = self.ParamTree.param(unicode(self.tr(u'Figures Shape'))).value()
        fig_size = self.ParamTree.param(unicode(self.tr(u'Figures Size'))).value()

        x_coords = [e[i] for e in self.data]
        y_coords = [e[j] for e in self.data]
        xmin, xmax = min(x_coords), max(x_coords)
        ymin, ymax = min(y_coords), max(y_coords)
        xshift = (xmax-xmin)*0.15
        yshift = (ymax-ymin)*0.15

        self.scatter_plot = pg.ScatterPlotItem(x=x_coords,y=y_coords,data=numpy.arange(len(x_coords)),size=fig_size,symbol=shape,brush=(pg.mkBrush(color)))
        self.scatter_plot.sigClicked.connect(self.elementFigureClicked)

        elems = self.scatter_plot.points()
        if self.previousSelectedElement > 0 and self.previousSelectedElement < len(elems):
            elems[self.previousSelectedElement].setBrush(pg.mkBrush("FFF"))


        text_size = {'color':'#FFF', 'font-size': str(self.font.pointSize())+'pt'}

        self.widget.getPlotItem().getAxis("bottom").setLabel(text=str(self.columns[i]),**text_size)
        self.widget.getPlotItem().getAxis("left").setLabel(text=str(self.columns[j]),**text_size)

        self.widget.addItem(self.scatter_plot)
        self.widget.getPlotItem().setRange(xRange=(xmin-xshift,xmax+xshift),yRange=(ymin-yshift,ymax+yshift))
        self.widget.removeSelectionRect()
        self.widget.addSelectionRect()

    @pyqtSlot()
    def on_actionMark_Selected_Elements_As_triggered(self):
        """
        @return: the indexes of the selected elements in the graph
        """
        if self.scatter_plot is None:
            return []

        rect = self.widget.ElementSelectionRect.rect()
        #the width and height could be negatives
        x1, y1 = rect.x(),rect.y()
        x2, y2 = x1 + rect.width(),y1 + rect.height()
        x1, x2, y1, y2 = min(x1,x2),max(x1,x2),min(y1,y2),max(y1,y2)

        selected_elements = [x.data() for x in self.scatter_plot.points() if x.pos().x() >= x1 and x.pos().x() <= x2 and x.pos().y() >= y1 and x.pos().y() <= y2]

        if len(selected_elements) == 0:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Warning", "There is no element selected.")
            return

        # get the selection
        editCategDialog = editCateg.Ui_Dialog()
        editCategDialogWindow = EditCategoriesDialog(self)
        editCategDialog.setupUi(editCategDialogWindow)
        widget = QWidget()
        self.clasiffCategories_vlayout = QtGui.QVBoxLayout()
        self.selection_widgets = []
        for k in self.classificationData.categories.keys():
            a = EditCategoriesWidget(self, k, self.classificationData,selectionOnly=True)
            # a.setStyleSheet("background-color:#EEF")
            self.selection_widgets.append(a)
            self.clasiffCategories_vlayout.addWidget(a)

        editCategDialog.bttnAddCategory.clicked.connect(self.addCategory)

        widget.setLayout(self.clasiffCategories_vlayout)
        editCategDialog.listWidget.setWidget(widget)
        editCategDialogWindow.exec_()
        d = dict([(x.categoryName,self.classificationData.categories[x.categoryName][x.comboCategories.currentIndex()])\
                  for x in self.selection_widgets if x.comboCategories.count()>0])
        self.elementsClasification.emit(selected_elements,d)

    def addCategory(self):
        dialog = QtGui.QDialog(self)
        dialog.setWindowTitle(unicode(self.tr(u"Create New Category")))
        layout = QtGui.QVBoxLayout()
        layout.addWidget(QtGui.QLabel(unicode(self.tr(u"Insert the name of the new Category"))))
        text = QtGui.QLineEdit()
        layout.addWidget(text)
        butts = QtGui.QDialogButtonBox()

        butts.addButton(QtGui.QDialogButtonBox.Ok)
        butts.addButton(QtGui.QDialogButtonBox.Cancel)
        QtCore.QObject.connect(butts, QtCore.SIGNAL("accepted()"), dialog.accept)
        QtCore.QObject.connect(butts, QtCore.SIGNAL("rejected()"), dialog.reject)

        layout.addWidget(butts)
        dialog.setLayout(layout)
        if dialog.exec_():
            category = str(text.text())
            if category == "":
                QtGui.QMessageBox.warning(QtGui.QMessageBox(), unicode(self.tr(u"Error")), unicode(self.tr(u"Invalid Category Name.")))
                return
            if self.clasiffCategories_vlayout and self.classificationData.addCategory(category):
                w = EditCategoriesWidget(self, category,self.classificationData)
                self.selection_widgets.append(w)
                self.clasiffCategories_vlayout.addWidget(w)

    def elementFigureClicked(self,x,y):
        self.selectElement(y[0].data())
        self.elementSelected.emit(y[0].data())


