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

        self.flag_action = QtGui.QAction(self)
        self.flag_action.setSeparator(True)
        self.addAction(self.flag_action)

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
        if actionGroup in [x.actionGroup for x in self.actions_groups]:
            return

        # set to not exclusive actions groups
        actionGroup.setExclusive(False)

        # create the group action manager for customize its visualization
        manager_act = QtGui.QAction(name, self)
        manager_act.setCheckable(True)

        # add into the toolbar
        self.actions_groups.append(GroupActionManager(manager_act, actionGroup))

        # connect to the change of visible state to customize the action group
        manager_act.toggled.connect(lambda checked_state: self.changeActionsVisibility(
                                                         actionGroup, checked_state))
        # actions visible by default
        manager_act.setChecked(True)

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

        # remove to maintain the order of the actions
        for action_manager in self.actions_groups:
            for act in action_manager.actionGroup.actions():
                self.removeAction(act)

        active_actions_groups = [x.actionGroup for x in self.actions_groups if x.actionManager.isChecked()]

        # add the actions
        for action_group in active_actions_groups:
            for act in action_group.actions():
                self.insertAction(self.flag_action, act)

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