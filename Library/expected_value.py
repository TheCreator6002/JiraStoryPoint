import numpy


class ExpectedValue:

    def __init__(self, input_array):
        if not isinstance(input_array, list):
            raise Exception('input data is not list type!')

        self._input_array = input_array
        self._result = 0

    def get_expected_value(self):
        self._result = numpy.mean(self._input_array)
        return round(float(self._result), 2)
