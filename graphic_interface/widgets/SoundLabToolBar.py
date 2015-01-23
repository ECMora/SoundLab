from PyQt4 import QtGui
from PyQt4 import QtCore


class GroupActionManager:
    """
    The group action manager is an container to handle the presence of a group of actions
    in a SoundLab toolbar
    Contains a (Checkable) action that manage an action group.
    This action manager enables or disables the presence of its
    associated action group in the toolbar
    """
    def __init__(self, actionManager=None, actionGroup=None):
        """
        """
        self.actionManager = actionManager
        self.actionGroup = actionGroup


class SoundLabToolBarWidget(QtGui.QToolBar):
    """
    Class that extends Toolbar behavior to provide a customizable
    Toolbar with groups of actions that could be change its visible state.

    """

    def __init__(self, parent=None):
        QtGui.QToolBar.__init__(self,parent)

        # the group of items actions to manage
        # list of GroupActionManager
        self.actions_groups = []

        # the list of actions that always would be visible and do not
        # belong to any group
        self.singleActions = []

        # the list of widgets that always would be visible and do not
        # belong to any group list of tuple (widget, widget action on toolbar)
        self.singleWidgets = []

        # manage internally the context menu
        # to show actions groups options
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

    def addAction(self, action):
        if action not in self.singleActions:
            self.singleActions.append(action)

        QtGui.QToolBar.addAction(self,action)

    def addWidget(self, widget):
        if widget in [x[0] for x in self.singleWidgets]:
            return

        widget_action = QtGui.QToolBar.addWidget(self, widget)

        self.singleWidgets.append((widget, widget_action))

    def addActionGroup(self, actionGroup, name=""):
        """
        Add an action Group to manage options of the actions in the toolbar
        :param actionGroup: The action group
        :param name: The name of the action group
        :return:
        """
        if actionGroup in [x.actionGroup for x in self.actions_groups]:
            return

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
        self.actions_groups.append(GroupActionManager(manager_act,actionGroup))

        # add the actions
        self.changeActionsVisibility(actionGroup, add_action=True)

    def changeActionsVisibility(self, actionGroup, add_action=True):
        """
        Add and removes from the tool bar the actions that belong to actionGroup,
        changing the visibility of that actions on the toolbar.
        :param actionGroup: the QActionGroup with the actions to add or remove from the toolbar
        :param add_action: If the action must be added into the toolbar. false otherwise.
        :return:
        """
        if not add_action:
            for action in actionGroup.actions():
                self.removeAction(action)
            return

        self.clear()

        for action_group in [x.actionGroup for x in self.actions_groups if x.actionManager.isChecked()]:
            for act in action_group.actions():
                self.addAction(act)

        for single_action in self.singleActions:
            self.addAction(single_action)

        for single_widget_action in [x[1] for x in self.singleWidgets]:
            single_widget_action.setVisible(True)

    def contextMenuEvent(self, QContextMenuEvent):
        """
        Implements the context menu event to show the
        action group visible state customization menu
        :param QContextMenuEvent:
        :return:
        """
        context_menu = QtGui.QMenu(self)

        # add an option for each action group added to the toolbar
        for act in [x.actionManager for x in self.actions_groups]:
            context_menu.addAction(act)

        # show the menu
        context_menu.popup(QContextMenuEvent.globalPos())
        QContextMenuEvent.accept()