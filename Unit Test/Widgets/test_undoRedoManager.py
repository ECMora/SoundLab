from unittest import TestCase
from graphic_interface.widgets.undo_redo_actions.UndoRedoActions import UndoRedoManager,UndoRedoAction


class TestUndoRedoManager(TestCase):
    def test_undo(self):
        self.fail()

    def test_redo(self):
        self.fail()

    def test_addAction(self):
        manager = UndoRedoManager()
        self.assertEqual(manager.count(),0,"Wrong Count")
        for x in range(50):
            oldcount = manager.count()
            manager.add(UndoRedoAction(lambda :None,lambda :None))
            self.assertEqual(manager.count(),oldcount+1,"Wrong Count")
        self.assertEqual(manager.count(),50,"Wrong count")

    def test_clearActions(self):
        self.fail()

    def test_count(self):
        self.fail()