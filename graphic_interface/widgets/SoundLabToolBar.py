from PyQt4 import QtGui
from PyQt4 import QtCore


class SoundLabToolBarWidget(QtGui.QToolBar):
    """

    """

    def __init__(self, parent=None):
        QtGui.QToolBar.__init__(self,parent)
        self.actions_groups = []
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

    def addActionGroup(self, actionGroup, name=""):
        """
        Add an action Group to manage options of the actions in the toolbar
        :param actionGroup: The action group
        :param name: The name of the action group
        :return:
        """
        if actionGroup in self.actions_groups:
            return

        # set to not exclusive actions groups
        actionGroup.setExclusive(False)

        # add on the toolbar context menu
        manager_act = QtGui.QAction(name, self)
        manager_act.setCheckable(True)
        manager_act.setChecked(True)
        manager_act.toggled.connect(lambda checked_state: actionGroup.setVisible(checked_state))

        self.actions_groups.append(manager_act)

    def contextMenuEvent(self, QContextMenuEvent):
        context_menu = QtGui.QMenu(self)
        for act in self.actions_groups:
            context_menu.addAction(act)

        context_menu.popup(QContextMenuEvent.globalPos())
        QContextMenuEvent.accept()
