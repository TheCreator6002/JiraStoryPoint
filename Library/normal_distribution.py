import math


class NormalDistribution:

    def __init__(self, input_value, expected_value, standard_deviation):
        self._input_value = input_value
        self._expected_value = expected_value
        self._standard_deviation = standard_deviation
        self._result = 0

    def get_normal_distribution(self):
        self._result = (1 + math.erf((self._input_value - self._expected_value) / math.sqrt(2) / self._standard_deviation)) / 2
        return self._result
