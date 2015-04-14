from unittest import TestCase
from PyQt4.QtGui import QApplication
from graphic_interface.widgets.QSignalDetectorWidget import QSignalDetectorWidget
from sound_lab_core.Elements.OneDimensionalElements.OneDimensionalElement import OneDimensionalElement

__author__ = 'y.febles'


class TestQSignalDetectorWidget(TestCase):
    def test_elements(self):
        app = QApplication([])
        widget = QSignalDetectorWidget(None)
        elements = []
        widget.elements = elements
        self.assertEqual(len(widget.elements), 0)

        elements = [OneDimensionalElement(None, 0, 10) for _ in range(10)]
        widget.elements = elements
        self.assertEqual(len(widget.elements), 10)
        self.assertEqual(all([isinstance(x, tuple) for x in widget.elements]), True)

    def test_draw_elements(self):
        self.fail()

    def test__get_no_visible_visual_items_tuples(self):
        app = QApplication([])
        widget = QSignalDetectorWidget(None)
        self.assertEqual(widget._get_no_visible_visual_items_tuples([]), [])

    def test_get_no_visible_visual_item(self):
        self.fail()

    def test_add_visual_elements(self):
        self.fail()

    def test_remove_visual_elements(self):
        self.fail()

    def test_add_parameter_visual_items(self):
        self.fail()

    def test_add_segmentation_items(self):
        self.fail()

    def test_delete_selected_elements(self):
        app = QApplication([])
        widget = QSignalDetectorWidget(None)
        elements = [OneDimensionalElement(None, 5 * x, 10 * x) for x in range(10)]
        print([(5 * x, 10 * x) for x in range(10)])
        widget.elements = elements
        widget.mainCursor.min, widget.mainCursor.max = 0, 100
        widget.zoomCursor.min, widget.zoomCursor.max = 0, 100
        self.assertEqual(widget.selectedRegion, (0, 100))
        widget.delete_selected_elements()
        self.assertEqual(len(widget.elements), 0)

    def test_mark_region_as_element(self):
        app = QApplication([])
        widget = QSignalDetectorWidget(None)
        elements = [OneDimensionalElement(None, 5 * x, 10 * x) for x in range(10)]
        widget.elements = elements
        index = widget.mark_region_as_element((910, 95))
        self.assertIsNone(index)
        index = widget.mark_region_as_element((1, 2))
        self.assertEqual(len(widget.elements), 11)
        self.assertEqual(index, 1)


