import unittest
from Library.expected_value import ExpectedValue
from Tests.test_data import result_set


class TestNormalDistribution(unittest.TestCase):

    def setUp(self):
        self.normal_distribution_first = ExpectedValue(input_array=result_set[0])
        self.normal_distribution_second = ExpectedValue(input_array=result_set[1])
        self.normal_distribution_third = ExpectedValue(input_array=result_set[2])

    def test_expected_value(self):
        self.assertEqual(self.normal_distribution_first.get_expected_value(), 10.91)
        self.assertEqual(self.normal_distribution_second.get_expected_value(), 8.01)
        self.assertEqual(self.normal_distribution_third.get_expected_value(), 7.72)
