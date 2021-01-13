import pandas


class BlockFormation:

    def __init__(self, period, data):
        self._result_block = []
        self._data = data
        self._period = period
        self._years = ['2013-01-01',
                       '2014-01-01',
                       '2015-01-01',
                       '2016-01-01',
                       '2017-01-01',
                       '2018-01-01',
                       '2019-01-01',
                       '2020-01-01',
                       '2021-01-01']
        self._quart = ['2013-01-01',
                       '2013-04-01',
                       '2013-07-01',
                       '2013-10-01',
                       '2014-01-01',
                       '2014-04-01',
                       '2014-07-01',
                       '2014-10-01',
                       '2015-01-01',
                       '2015-04-01',
                       '2015-07-01',
                       '2015-10-01',
                       '2016-01-01',
                       '2016-04-01',
                       '2016-07-01',
                       '2016-10-01',
                       '2017-01-01',
                       '2017-04-01',
                       '2017-07-01',
                       '2017-10-01',
                       '2018-01-01',
                       '2018-04-01',
                       '2018-07-01',
                       '2018-10-01',
                       '2019-01-01',
                       '2019-04-01',
                       '2019-07-01',
                       '2019-10-01',
                       '2020-01-01',
                       '2020-04-01',
                       '2020-07-01',
                       '2020-10-01',
                       '2021-01-01',
                       '2021-04-01',
                       '2021-07-01',
                       '2021-10-01']

    def get_block(self):
        if self._period == 'years':
            self._result_block = BlockFormation.__formation(self._years, self._data)
            return self._result_block
        elif self._period == 'quarts':
            self._result_block = BlockFormation.__formation(self._quart, self._data)
            return self._result_block

    @staticmethod
    def __formation(period, data):
        result = []
        for i in range(len(period) - 1):
            iteration_result = data[
                (data['Start'] > period[i]) &
                (data['Start'] < period[i + 1])]
            result.append(iteration_result['SPHours'].values.tolist())
        return result
