from unittest import TestCase
from graphic_interface.widgets.undo_redo_actions.UndoRedoActions import UndoRedoManager, UndoRedoAction

__author__ = 'y.febles'


class TestUndoRedoManager(TestCase):
    def test_undo(self):
        manager = UndoRedoManager()

        manager.add(UndoRedoAction())

        self.assertEqual(manager.count(), 1, "Wrong count")
        manager.undo()
        self.assertEqual(manager.count(), 1, "The undo action must not change the number of stored actions")

    def test_undo_severalActions(self):
        manager = UndoRedoManager()

        for x in range(30):
            manager.add(UndoRedoAction())

        self.assertEqual(manager.count(), 30, "Wrong count")
        try:
            for i in range(30):
                manager.undo()
        except:
            self.fail("Undo raise exception")

        self.assertEqual(manager.count(), 30, "The undo action must not change the number of stored actions")

    def test_redo(self):
        manager = UndoRedoManager()

        manager.add(UndoRedoAction())

        self.assertEqual(manager.count(), 1, "Wrong count")
        manager.redo()
        self.assertEqual(manager.count(), 1, "The redo action must not change the number of stored actions")

    def test_redo_severalActions(self):
        manager = UndoRedoManager()

        for x in range(30):
            manager.add(UndoRedoAction())

        self.assertEqual(manager.count(), 30, "Wrong count")
        try:
            for i in range(30):
                manager.redo()
        except:
            self.fail("redo raise exception")

        self.assertEqual(manager.count(), 30, "The redo action must not change the number of stored actions")

    def test_add(self):
        manager = UndoRedoManager()
        self.assertEqual(manager.count(), 0, "Wrong Count")

        for x in range(50):
            oldcount = manager.count()
            manager.add(UndoRedoAction())
            self.assertEqual(manager.count(), oldcount + 1, "Wrong Count")

        self.assertEqual(manager.count(), 50, "Wrong count")

    def test_clear(self):
        manager = UndoRedoManager()

        for i in range(5):
            for x in range(20):
                manager.add(UndoRedoAction())

            self.assertEqual(manager.count(), 20, "Wrong count")
            manager.clear()
            self.assertEqual(manager.count(), 0, "The count must be 0 after clear")
