"""
Author: qiacai
"""

import math
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

from ada_core import exceptions, utils, constants
from ada_core.algorithms import Algorithm
from ada_core.data_model.io_data_type import AlgorithmIODataType
from ada_core.data_model.time_series import TimeSeries


class TimeOffset(Algorithm):

    def __init__(self):
        super(TimeOffset, self).__init__(self.__class__.__name__)
        # self.name = 'time_offset'

    def _run_algorithm(self, input_value, offset=None):

        if offset is None:
            offset = constants.ALGORITHM_DEFAULT_CALCULATOR_TIME_OFFSET_OFFSET

        output_value = TimeSeries()
        for timestamp, value in input_value.items():
            output_value.update({timestamp + offset: value})
        return output_value


class StandardNormalization(Algorithm):

    def __init__(self):
        super(StandardNormalization, self).__init__(self.__class__.__name__)
        # self.name = 'standard_normalization'

    def _run_algorithm(self, input_value):

        output_value = TimeSeries()

        mean = np.asscalar(np.average(input_value.getValueList()))
        std = np.asscalar(np.std(input_value.getValueList()))

        if std <= 0:
            for timestamp, value in input_value.items():
                output_value.update({timestamp: value})
        else:
            for timestamp, value in input_value.items():
                output_value.update({timestamp: (value - mean) / std})

        return output_value


class ScaleNormalization(Algorithm):

    def __init__(self):
        super(ScaleNormalization, self).__init__(self.__class__.__name__)
        # self.name = 'scale_normalization'

    def _run_algorithm(self, input_value):

        output_value = TimeSeries()
        max = np.asscalar(np.max(input_value.getValueList()))
        min = np.asscalar(np.min(input_value.getValueList()))

        if max <= min:
            for timestamp, value in input_value.items():
                output_value.update({timestamp: value})
        else:
            for timestamp, value in input_value.items():
                output_value.update({timestamp: (value - min) / (max - min)})

        return output_value


class ExponentialSmooth(Algorithm):

    """
    return a new time series which is a exponential smoothed version of the original data series.
    soomth forward once, backward once, and then take the average.

    :param float smoothing_factor: smoothing factor
    :return: :class:`TimeSeries` object.
    """

    def __init__(self):
        super(ExponentialSmooth, self).__init__(self.__class__.__name__)
        # self.name = 'exponential_smooth'

    def _run_algorithm(self, input_value, smoothing_factor=None):

        if smoothing_factor is None:
            smoothing_factor = constants.ALGORITHM_DEFAULT_CALCULATOR_TIME_OFFSET_OFFSET

        forward_smooth = {}
        backward_smooth = {}
        output_value = {}

        pre_entry = input_value.getValueList()[0]
        next_entry = input_value.getValueList()[-1]

        for key, value in input_value.items():
            forward_smooth[key] = smoothing_factor * pre_entry + (1 - smoothing_factor) * value
            pre_entry = forward_smooth[key]
        for key, value in input_value.items():
            backward_smooth[key] = smoothing_factor * next_entry + (1 - smoothing_factor) * value
            next_entry = backward_smooth[key]
        for key in forward_smooth.keys():
            output_value[key] = (forward_smooth[key] + backward_smooth[key]) / 2
        return TimeSeries(output_value)


class SeasonalDecompose(Algorithm):

    def __init__(self):
        super(SeasonalDecompose, self).__init__(self.__class__.__name__)
        # self.name = 'seasonal_decompose'

    def _run_algorithm(self, input_value, freq=None, trend_only=None, is_fillna=None):

        if freq is None:
            freq = constants.ALGORITHM_DEFAULT_CALCULATOR_SEASONAL_DECOMPOSE_FREQ

        if trend_only is None:
            trend_only = constants.ALGORITHM_DEFAULT_CALCULATOR_SEASONAL_DECOMPOSE_TREND_ONLY

        if is_fillna is None:
            is_fillna = constants.ALGORITHM_DEFAULT_CALCULATOR_SEASONAL_DECOMPOSE_FILLNA

        if len(input_value) <= freq:
            raise exceptions.ParametersNotPassed('ada.algorithms.transformer.seasonal_decompose: '
                                                   'the lengh of the original time series is less than one period')

        valueList = input_value.getValueList()
        valueList = [valueList.median() if math.isnan(value) else value for value in valueList]
        results = seasonal_decompose(valueList, freq=freq, two_sided=False, model='additive')

        if trend_only:
            time_series = results.trend
        else:
            time_series = results.trend + results.resid

        time_series = pd.Series(time_series, input_value.getKeyList())

        if is_fillna:
            time_series = time_series.fillna(method='bfill')
        else:
            time_series = time_series[freq:]

        return TimeSeries(dict(time_series.to_dict()))