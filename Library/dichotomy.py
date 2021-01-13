from Library.expected_value import ExpectedValue
from Library.standard_deviation import StandardDeviation
from Library.normal_distribution import NormalDistribution
import math


class Dichotomy:

    def __init__(self, input_array, error, max_step, forecasting_accuracy):
        self._input_array = input_array
        self._expected_value = ExpectedValue(input_array=input_array).get_expected_value()
        self._standard_deviation = StandardDeviation(input_array=input_array).get_deviation()
        self._left_border = self._expected_value
        self._right_border = self._expected_value + math.pow(self._standard_deviation, 2)
        self.error = error
        self.max_step = max_step
        self._forecasting_accuracy = forecasting_accuracy
        self._result = 0

    def find_root(self):
        if not self._input_array:
            return 0

        if len(self._input_array) == 1:
            return 0
        else:

            Dichotomy.__log_value(self._forecasting_accuracy)

            step = 0
            function_value_left = self._function_computation(input_value=self._left_border)
            function_value_right = self._function_computation(input_value=self._right_border)
            if not self._zero_crossing(function_value_left, function_value_right):
                print('Warning! Returned expected value = ' + str(self._expected_value))
                return self._expected_value

            while self._right_border - self._left_border > self.error and step < self.max_step:
                self._sub_interval_exclusion(function_value_left=function_value_left)
                step += 1

            root_search_result = self._get_middle_of_interval(left_border=self._left_border,
                                                              right_border=self._right_border)
            return root_search_result

    def _sub_interval_exclusion(self, function_value_left):
        middle_of_interval = self._get_middle_of_interval(left_border=self._left_border,
                                                          right_border=self._right_border)
        function_middle_of_interval = self._function_computation(input_value=middle_of_interval)

        if self._zero_crossing(function_value_left, function_middle_of_interval):
            self._right_border = middle_of_interval
        else:
            self._left_border = middle_of_interval

    def _function_computation(self, input_value):
        function_value = NormalDistribution(input_value=input_value,
                                            expected_value=self._expected_value,
                                            standard_deviation=self._standard_deviation).get_normal_distribution()
        result = function_value - self._forecasting_accuracy
        return result

    @staticmethod
    def _zero_crossing(first_function_value, second_function_value):
        result = first_function_value * second_function_value <= 0
        return result

    @staticmethod
    def _get_middle_of_interval(left_border, right_border):
        value_middle_of_interval = (left_border + right_border) / 2
        return value_middle_of_interval

    @staticmethod
    def __log_value(value):
        print("Find root at value forecasting accuracy: " + str(value))
