from PyQt4 import QtGui
from PyQt4 import QtCore


class SoundLabToolBarWidget(QtGui.QToolBar):
    """
    Class that extends Toolbar behavior to provide a customizable
    Toolbar with groups of actions that could be change its visible state
    """

    def __init__(self, parent=None):
        QtGui.QToolBar.__init__(self,parent)
        # the group of actions to manage
        self.actions_groups = []

        # manage internally the context menu
        # to show actions groups options
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
        # add the actions
        self.changeActionsVisibility(actionGroup,add_action=True)

        # set to not exclusive actions groups
        actionGroup.setExclusive(False)

        # create the group action manager for customize its visualization
        manager_act = QtGui.QAction(name, self)
        manager_act.setCheckable(True)
        # actions visible by default
        manager_act.setChecked(True)

        # connect to the change of visible state to customize the action group
        manager_act.toggled.connect(lambda checked_state: self.changeActionsVisibility(
                                                         actionGroup, checked_state))
        # add into the toolbar
        self.actions_groups.append(manager_act)

    def changeActionsVisibility(self, actionGroup, add_action=True):
        """
        Add and removes from the tool bar the actions that belong to actionGroup,
        changing the visibility of that actions on the toolbar.
        :param actionGroup: the QActionGroup with the actions to add or remove from the toolbar
        :param add_action: If the action must be added into the toolbar. false otherwise.
        :return:
        """

        for action in actionGroup.actions():
            if add_action:
                self.addAction(action)
            else:
                self.removeAction(action)

    def contextMenuEvent(self, QContextMenuEvent):
        """
        Implements the context menu event to show the
        action group visible state customization menu
        :param QContextMenuEvent:
        :return:
        """
        context_menu = QtGui.QMenu(self)

        # add an option for each action group added to the toolbar
        for act in self.actions_groups:
            context_menu.addAction(act)

        # show the menu
        context_menu.popup(QContextMenuEvent.globalPos())
        QContextMenuEvent.accept()
