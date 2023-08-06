"""
Author: qiacai
"""

import pytz

from schematics.models import Model
from schematics.types import StringType, ModelType
from schematics.exceptions import ConversionError, BaseError, CompoundError, ValidationError

from ada_core import exceptions, utils, constants
from ada_core.data_model.io_data_type import AlgorithmIODataType
from ada_core.algorithms import *


__all__ = ['BoolNaiveAlgorithmMeta', 'NumNaiveAlgorithmMeta', 'TsNaiveAlgorithmMeta', 'EntryNaiveAlgorithmMeta',
           'BoolANDLogicBinaryJudgeAlgorithmMeta', 'BoolORLogicBinaryJudgeAlgorithmMeta', 'BoolXORLogicBinaryJudgeAlgorithmMeta',
           'NumEqualsBinaryJudgeAlgorithmMeta', 'EntryEqualsBinaryJudgeAlgorithmMeta', 'TsEqualsBinaryJudgeAlgorithmMeta',
           'NumGreaterThansJudgeAlgorithmMeta', 'EntryGreaterThansJudgeAlgorithmMeta', 'TsGreaterThansJudgeAlgorithmMeta', 'EntryNumGreaterThansJudgeAlgorithmMeta', 'TsNumGreaterThansJudgeAlgorithmMeta',
           'NumGreaterThanOrEqualsBinaryJudgeAlgorithmMeta', 'EntryGreaterThanOrEqualsBinaryJudgeAlgorithmMeta', 'TsGreaterThanOrEqualsBinaryJudgeAlgorithmMeta', 'EntryNumGreaterThanOrEqualsBinaryJudgeAlgorithmMeta', 'TsNumGreaterThanOrEqualsBinaryJudgeAlgorithmMeta',
           'NumLessThansBinaryJudgeAlgorithmMeta', 'EntryLessThansBinaryJudgeAlgorithmMeta', 'TsLessThansBinaryJudgeAlgorithmMeta', 'EntryNumLessThansBinaryJudgeAlgorithmMeta', 'TsNumLessThansBinaryJudgeAlgorithmMeta',
           'NumLessThanOrEqualsBinaryJudgeAlgorithmMeta', 'EntryLessThanOrEqualsBinaryJudgeAlgorithmMeta', 'TsLessThanOrEqualsBinaryJudgeAlgorithmMeta', 'EntryNumLessThanOrEqualsBinaryJudgeAlgorithmMeta', 'TsNumLessThanOrEqualsBinaryJudgeAlgorithmMeta',
           'MeanAlgorithmMeta', 'MedianAlgorithmMeta', 'MaxAlgorithmMeta', 'MinAlgorithmMeta', 'CushionAlgorithmMeta',
           'PercentileAlgorithmMeta', 'StdAlgorithmMeta', 'MadAlgorithmMeta', 'CountAlgorithmMeta', 'SumAlgorithmMeta',
           'ValueScaleAlgorithmMeta', 'TimeOffsetAlgorithmMeta', 'StandardNormalizationAlgorithmMeta',
           'ScaleNormalizationAlgorithmMeta', 'ExponentialSmoothAlgorithmMeta', 'SeasonalDecomposeAlgorithmMeta',
           'EntryHardThresholdAlgorithmMeta', 'TsHardThresholdAlgorithmMeta', 'NumHardThresholdAlgorithmMeta',
           'SoftThresholdAlgorithmMeta', 'CushionThresholdAlgorithmMeta'
           ]


class BoolNaiveAlgorithmMeta(Model):
    alg_name = 'naive'
    input_value = AlgorithmIODataType.BOOL.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_cls = naive_algorithm.NaiveAlgorithm


class NumNaiveAlgorithmMeta(Model):
    alg_name = 'naive'
    input_value = AlgorithmIODataType.FLOAT.value(required=True)
    output_value = AlgorithmIODataType.FLOAT.value()
    alg_cls = naive_algorithm.NaiveAlgorithm


class TsNaiveAlgorithmMeta(Model):
    alg_name = 'naive'
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.TIME_SERIES.value()
    alg_cls = naive_algorithm.NaiveAlgorithm


class EntryNaiveAlgorithmMeta(Model):
    alg_name = 'naive'
    input_value = AlgorithmIODataType.ENTRY.value(required=True)
    output_value = AlgorithmIODataType.ENTRY.value()
    alg_cls = naive_algorithm.NaiveAlgorithm


class BoolANDLogicBinaryJudgeAlgorithmMeta(Model):
    alg_name = 'and'
    alg_cls = binary_judge_algorithms.ANDLogicBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_BOOL_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class BoolORLogicBinaryJudgeAlgorithmMeta(Model):
    alg_name = 'and'
    alg_cls = binary_judge_algorithms.ORLogicBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_BOOL_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class BoolXORLogicBinaryJudgeAlgorithmMeta(Model):
    alg_name = 'and'
    alg_cls = binary_judge_algorithms.XORLogicBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_XOR_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class NumEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '=='
    alg_cls = binary_judge_algorithms.EqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_NUMBER_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class EntryEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '=='
    alg_cls = binary_judge_algorithms.EqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_ENTRY_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class TsEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '=='
    alg_cls = binary_judge_algorithms.EqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_TS_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class EntryNumEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '=='
    alg_cls = binary_judge_algorithms.EqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_ENTRT_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class TsNumEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '=='
    alg_cls = binary_judge_algorithms.EqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_TS_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class NumGreaterThansBinaryJudgeAlgorithmMeta(Model):
    alg_name = '>'
    alg_cls = binary_judge_algorithms.GreaterThansBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class EntryGreaterThansBinaryJudgeAlgorithmMeta(Model):
    alg_name = '>'
    alg_cls = binary_judge_algorithms.GreaterThansBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_ENTRY_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class TsGreaterThansBinaryJudgeAlgorithmMeta(Model):
    alg_name = '>'
    alg_cls = binary_judge_algorithms.GreaterThansBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_TS_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class EntryNumGreaterThansBinaryJudgeAlgorithmMeta(Model):
    alg_name = '>'
    alg_cls = binary_judge_algorithms.GreaterThansBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_ENTRT_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class TsNumGreaterThansBinaryJudgeAlgorithmMeta(Model):
    alg_name = '>'
    alg_cls = binary_judge_algorithms.GreaterThansBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_TS_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class NumGreaterThanOrEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '>='
    alg_cls = binary_judge_algorithms.GreaterThanOrEqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class EntryGreaterThanOrEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '>='
    alg_cls = binary_judge_algorithms.GreaterThanOrEqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_ENTRY_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class TsGreaterThanOrEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '>='
    alg_cls = binary_judge_algorithms.GreaterThanOrEqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_TS_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class EntryNumGreaterThanOrEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '>='
    alg_cls = binary_judge_algorithms.GreaterThanOrEqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_ENTRT_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class TsNumGreaterThanOrEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '>='
    alg_cls = binary_judge_algorithms.GreaterThanEqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_TS_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class NumLessThansBinaryJudgeAlgorithmMeta(Model):
    alg_name = '<'
    alg_cls = binary_judge_algorithms.LessThansBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class EntryLessThansBinaryJudgeAlgorithmMeta(Model):
    alg_name = '<'
    alg_cls = binary_judge_algorithms.LessThansBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_ENTRY_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class TsLessThansBinaryJudgeAlgorithmMeta(Model):
    alg_name = '<'
    alg_cls = binary_judge_algorithms.LessThansBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_TS_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class EntryNumLessThansBinaryJudgeAlgorithmMeta(Model):
    alg_name = '<'
    alg_cls = binary_judge_algorithms.LessThansBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_ENTRT_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class TsNumLessThansBinaryJudgeAlgorithmMeta(Model):
    alg_name = '<'
    alg_cls = binary_judge_algorithms.LessThansBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_TS_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class NumLessThanOrEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '<='
    alg_cls = binary_judge_algorithms.LessThanOrEqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class EntryLessThanOrEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '<='
    alg_cls = binary_judge_algorithms.LessThanOrEqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_ENTRY_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class TsLessThanOrEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '<='
    alg_cls = binary_judge_algorithms.LessThanOrEqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_TS_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class EntryNumLessThanOrEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '<='
    alg_cls = binary_judge_algorithms.LessThanOrEqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_ENTRT_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class TsNumLessThanOrEqualsBinaryJudgeAlgorithmMeta(Model):
    alg_name = '<='
    alg_cls = binary_judge_algorithms.LessThanOrEqualsBinaryJudgeAlgorithm
    input_value = AlgorithmIODataType.BINARY_TS_NUM_INPUT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()


class TsValueScaleAlgorithmMeta(Model):
    alg_name = 'value_scale'
    alg_cls = binary_num1ts2ts_calculate_algorithms.ValueScale
    operator = StringType(choices=['+', '-', '*', '/'], required=True)
    input_value = AlgorithmIODataType.BINARY_NUMBER_TS_INPUT.value(required=True)
    output_value = AlgorithmIODataType.TIME_SERIES.value()


class EntryValueScaleAlgorithmMeta(Model):
    alg_name = 'value_scale'
    alg_cls = binary_num1ts2ts_calculate_algorithms.ValueScale
    operator = StringType(choices=['+', '-', '*', '/'], required=True)
    input_value = AlgorithmIODataType.BINARY_NUMBER_ENTRY_INPUT.value(required=True)
    output_value = AlgorithmIODataType.TIME_SERIES.value()


class BaseUnaryTs2NumCalAlgorithmMeta(Model):
    alg_name = 'base_unary_ts2num_calculate'
    alg_cls = unary_ts2num_calculate_algorithms.BaseUnaryTs2NumCalAlgorithm
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.FLOAT.value()


class MeanAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'mean'
    alg_cls = unary_ts2num_calculate_algorithms.Mean
    default = AlgorithmIODataType.FLOAT.value()


class MedianAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'median'
    alg_cls = unary_ts2num_calculate_algorithms.Median
    default = AlgorithmIODataType.FLOAT.value()


class MaxAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'max'
    alg_cls = unary_ts2num_calculate_algorithms.Max
    default = AlgorithmIODataType.FLOAT.value()


class MinAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'min'
    alg_cls = unary_ts2num_calculate_algorithms.Min
    default = AlgorithmIODataType.FLOAT.value()


class PercentileAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'percentile'
    alg_cls = unary_ts2num_calculate_algorithms.Percentile
    default = AlgorithmIODataType.FLOAT.value()
    percent = AlgorithmIODataType.INT.value(min_value=0, max_value=100, default=constants.ALGORITHM_DEFAULT_CALCULATOR_PERCENTILE_PERCENTILE)


class StdAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'std'
    alg_cls = unary_ts2num_calculate_algorithms.Std
    default = AlgorithmIODataType.FLOAT.value()


class MadAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'mad'
    alg_cls = unary_ts2num_calculate_algorithms.Mad
    default = AlgorithmIODataType.FLOAT.value()


# Not Fully Implemented
class CushionAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'cushion'
    alg_cls = unary_ts2num_calculate_algorithms.Cushion
    default = AlgorithmIODataType.FLOAT.value()
    upper_percentile = AlgorithmIODataType.INT.value(min_value=0, max_value=100)
    lower_percentile = AlgorithmIODataType.INT.value(min_value=0, max_value=100)
    is_upper = AlgorithmIODataType.BOOL.value(default=constants.ALGORITHM_DEFAULT_CALCULATOR_CUSHION_IS_UPPER)


class CountAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'count'
    alg_cls = unary_ts2num_calculate_algorithms.Count
    input_value = AlgorithmIODataType.INT.value()
    default = AlgorithmIODataType.INT.value()


class SumAlgorithmMeta(BaseUnaryTs2NumCalAlgorithmMeta):
    alg_name = 'sum'
    alg_cls = unary_ts2num_calculate_algorithms.Sum
    default = AlgorithmIODataType.FLOAT.value()


class BaseUnaryTs2TsCalAlgorithmMeta(Model):
    alg_name = 'base_unary_ts2ts_calculate'
    alg_cls = unary_ts2ts_calculate_algorithms.BaseUnaryTs2TsCalAlgorithm
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.TIME_SERIES.value()


class TimeOffsetAlgorithmMeta(BaseUnaryTs2TsCalAlgorithmMeta):
    alg_name = 'time_offset'
    alg_cls = unary_ts2ts_calculate_algorithms.TimeOffset
    offset = AlgorithmIODataType.INT.value(default=constants.ALGORITHM_DEFAULT_CALCULATOR_TIME_OFFSET_OFFSET)


class StandardNormalizationAlgorithmMeta(BaseUnaryTs2TsCalAlgorithmMeta):
    alg_name = 'standard_normalization'
    alg_cls = unary_ts2ts_calculate_algorithms.StandardNormalization


class ScaleNormalizationAlgorithmMeta(BaseUnaryTs2TsCalAlgorithmMeta):
    alg_name = 'scale_normalization'
    alg_cls = unary_ts2ts_calculate_algorithms.StandardNormalization


class ExponentialSmoothAlgorithmMeta(BaseUnaryTs2TsCalAlgorithmMeta):
    alg_name = 'exponential_smooth'
    alg_cls = unary_ts2ts_calculate_algorithms.ExponentialSmooth
    smoothing_factor = AlgorithmIODataType.FLOAT.value(min_value=0, max_value=1, default=constants.ALGORITHM_DEFAULT_CALCULATOR_EXPONENTIAL_SMOOTH_SMOOTHING_FACTOR)


class SeasonalDecomposeAlgorithmMeta(BaseUnaryTs2TsCalAlgorithmMeta):
    alg_name = 'seasonal_decompose'
    alg_cls = unary_ts2ts_calculate_algorithms.SeasonalDecompose
    freq = AlgorithmIODataType.INT.value(min_value=0, default=constants.ALGORITHM_DEFAULT_CALCULATOR_SEASONAL_DECOMPOSE_FREQ)
    trend_only = AlgorithmIODataType.BOOL.value(default=constants.ALGORITHM_DEFAULT_CALCULATOR_SEASONAL_DECOMPOSE_TREND_ONLY)
    is_fillna = AlgorithmIODataType.BOOL.value(default=constants.ALGORITHM_DEFAULT_CALCULATOR_SEASONAL_DECOMPOSE_FILLNA)


# Not Fully Implemented
class EntryHardThresholdAlgorithmMeta(Model):
    input_value = AlgorithmIODataType.ENTRY.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_name = 'hard_threshold'
    alg_cls = unary_judge_algorithms.HardThreshold
    operator = StringType(choices=['>', '>=', '<', '<=', '=='], required=True)
    threshold = AlgorithmIODataType.FLOAT.value(required=True, default=constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_THRESHOLD)


class TsHardThresholdAlgorithmMeta(Model):
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_name = 'hard_threshold'
    alg_cls = unary_judge_algorithms.HardThreshold
    operator = StringType(choices=['>', '>=', '<', '<=', '=='], required=True)
    threshold = AlgorithmIODataType.FLOAT.value(required=True)
    local_window = StringType(default=constants.ALGORITHM_DEFAULT_HARD_THRESHOLD_LOCAL_WINDOW, regex=constants.ALGORITHM_DEFAULT_WINDOW_REGEX)
    timezone = StringType(choices=pytz.all_timezones, default=constants.ALGORITHM_DEFAULT_TIMEZONE)


class NumHardThresholdAlgorithmMeta(Model):
    input_value = AlgorithmIODataType.FLOAT.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_name = 'hard_threshold'
    alg_cls = unary_judge_algorithms.HardThreshold
    operator = StringType(choices=['>', '>=', '<', '<=', '=='], required=True)
    threshold = AlgorithmIODataType.FLOAT.value(required=True)


class SoftThresholdAlgorithmMeta(Model):
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_name = 'soft_threshold'
    alg_cls = unary_judge_algorithms.SoftThreshold
    operator = StringType(choices=['>', '>=', '<', '<='], required=True)
    factor = AlgorithmIODataType.FLOAT.value(default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_FACTOR, min_value=0)
    local_window = StringType(default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_LOCAL_WINDOW, regex=constants.ALGORITHM_DEFAULT_WINDOW_REGEX)
    lag_window = StringType(default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_LAG_WINDOW, regex=constants.ALGORITHM_DEFAULT_WINDOW_REGEX)
    benchmark_method = StringType(choices=['mean', 'median'], default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_BENCHMARK_METHOD)
    bound_method = StringType(choices=['hard', 'std', 'mad', 'ratio'], default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_BOUND_METHOD)
    timezone = StringType(choices=pytz.all_timezones, default=constants.ALGORITHM_DEFAULT_SOFT_THRESHOLD_TIMEZONE)


class CushionThresholdAlgorithmMeta(Model):
    input_value = AlgorithmIODataType.TIME_SERIES.value(required=True)
    output_value = AlgorithmIODataType.BOOL.value()
    alg_name = 'cushion_threshold'
    alg_cls = unary_judge_algorithms.CushionThreshold
    operator = StringType(choices=['>', '>=', '<', '<='], required=True)
    local_window = StringType(default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_LOCAL_WINDOW, regex=constants.ALGORITHM_DEFAULT_WINDOW_REGEX)
    lag_window = StringType(default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_LAG_WINDOW, regex=constants.ALGORITHM_DEFAULT_WINDOW_REGEX)
    benchmark_method = StringType(choices=['mean', 'median'], default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_BENCHMARK_METHOD)
    bound_method = StringType(choices=['std', 'mad'], default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_BOUND_METHOD)
    factor = AlgorithmIODataType.FLOAT.value(default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_FACTOR, min_value=0)
    timezone = StringType(choices=pytz.all_timezones, default=constants.ALGORITHM_DEFAULT_CUSHION_THRESHOLD_TIMEZONE)
    upper_percentile = AlgorithmIODataType.INT.value(min_value=0, max_value=100)
    lower_percentile = AlgorithmIODataType.INT.value(min_value=0, max_value=100)