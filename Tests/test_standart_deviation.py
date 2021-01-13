import unittest
from Library.standard_deviation import StandardDeviation
from Tests.test_data import result_set


class TestStandardDeviation(unittest.TestCase):

    def setUp(self):
        self.normal_distribution_first = StandardDeviation(input_array=result_set[0])
        self.normal_distribution_second = StandardDeviation(input_array=result_set[1])
        self.normal_distribution_third = StandardDeviation(input_array=result_set[2])

    def test_expected_value(self):
        self.assertEqual(self.normal_distribution_first.get_deviation(), 11.16)
        self.assertEqual(self.normal_distribution_second.get_deviation(), 5.57)
        self.assertEqual(self.normal_distribution_third.get_deviation(), 4.28)
