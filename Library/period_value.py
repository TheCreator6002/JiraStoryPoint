import pandas
from Library.dichotomy import Dichotomy
from Library.block_formation import BlockFormation


class PeriodValue:
    def __init__(self, forecasting_accuracy, period: str, input_array, project):
        self.__forecasting_accuracy = forecasting_accuracy
        self.__columns = ['Result']
        self.__result = []
        self.__years = ['2013-01-01',
                        '2014-01-01',
                        '2015-01-01',
                        '2016-01-01',
                        '2017-01-01',
                        '2018-01-01',
                        '2019-01-01',
                        '2020-01-01']
        self.__quarts = ['2013-01-01',
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
                         '2021-07-01']
        self.__period = period
        self.__input_array = input_array
        self.__project = project
        self.__data_frame = 0

    def get_value(self):
        PeriodValue.__create_block(self)

        for i in range(len(self.__block)):
            dichotomy_result = Dichotomy(input_array=self.__block[i],
                                         error=0.0001,
                                         max_step=1000000,
                                         forecasting_accuracy=self.__forecasting_accuracy)
            self.__result.append(dichotomy_result.find_root())

        if self.__period == 'years':
            PeriodValue.__create_result_data_frame(self, self.__period, self.__years)

        elif self.__period == 'quarts':
            PeriodValue.__create_result_data_frame(self, self.__period, self.__quarts)

        return self.__data_frame

    def __create_block(self):
        self.__block = BlockFormation(period=self.__period, data=self.__input_array).get_block()

    def __create_result_data_frame(self, period, array):
        self.__data_frame = pandas.DataFrame(data=self.__result, columns=self.__columns)
        self.__data_frame['Date'] = array
        self.__data_frame['DateType'] = period
        self.__data_frame['ProjectType'] = str(self.__project)
        self.__data_frame['forecasting_accuracy'] = self.__forecasting_accuracy
