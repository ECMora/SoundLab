from unittest import TestCase

from sound_lab_core.Segmentation.OneDimensional.OneDimensionalElementsDetector import \
    OneDimensionalElementsDetector


class TestOneDimensionalElementsDetector(TestCase):
    def test_merge_intervals(self):
        x = OneDimensionalElementsDetector(None)

        intervals = []
        self.assertEqual(x.merge_intervals(intervals), [], "An empty list must return an empty result")

        # merge by 5 % of distance
        intervals = [(0, 10), (11, 21)]
        self.assertEqual(x.merge_intervals(intervals, 5), [(0, 21)], "")

        # merge multiple by 10 % of distance
        intervals = [(0, 10), (11, 21), (24, 40)]
        self.assertEqual(x.merge_intervals(intervals, 10), [(0, 40)], "")

        # merge by back to front
        intervals = [(0, 10), (11, 21), (30, 40), (50, 200)]
        self.assertEqual(x.merge_intervals(intervals, 10), [(0, 200)], "")

        # merge by back to front and multiple
        intervals = [(0, 10), (11, 21), (30, 40), (50, 60), (62, 70), (80, 200)]
        self.assertEqual(x.merge_intervals(intervals, 10), [(0, 200)], "")


