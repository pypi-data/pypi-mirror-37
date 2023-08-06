"""
Author: qiacai
"""


from ada_core.algorithms import Algorithm
from ada_core.data_model.entry import Entry
from ada_core.data_model.time_series import TimeSeries


class EqualsBinaryJudgeAlgorithm(Algorithm):
    def __init__(self):
        super(EqualsBinaryJudgeAlgorithm, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if isinstance(input_value.left, TimeSeries) or isinstance(input_value.left, Entry):
            return input_value.left.equals(input_value.right)
        elif isinstance(input_value.right, TimeSeries) or isinstance(input_value.right, Entry):
            return input_value.right.equals(input_value.left)
        else:
            return True if input_value.left == input_value.right else False


class GreaterThansBinaryJudgeAlgorithm(Algorithm):
    def __init__(self):
        super(GreaterThansBinaryJudgeAlgorithm, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if isinstance(input_value.left, TimeSeries) or isinstance(input_value.left, Entry):
            return input_value.left.greaterThans(input_value.right)
        elif isinstance(input_value.right, TimeSeries) or isinstance(input_value.right, Entry):
            return input_value.right.lessThans(input_value.left)
        else:
            return True if input_value.left > input_value.right else False


class GreaterThanOrEqualsBinaryJudgeAlgorithm(Algorithm):
    def __init__(self):
        super(GreaterThanOrEqualsBinaryJudgeAlgorithm, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if isinstance(input_value.left, TimeSeries) or isinstance(input_value.left, Entry):
            return input_value.left.greaterThanOrEquals(input_value.right)
        elif isinstance(input_value.right, TimeSeries) or isinstance(input_value.right, Entry):
            return input_value.right.lessThanOrEquals(input_value.left)
        else:
            return True if input_value.left >= input_value.right else False


class LessThansBinaryJudgeAlgorithm(Algorithm):
    def __init__(self):
        super(LessThansBinaryJudgeAlgorithm, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if isinstance(input_value.left, TimeSeries) or isinstance(input_value.left, Entry):
            return input_value.left.lessThans(input_value.right)
        elif isinstance(input_value.right, TimeSeries) or isinstance(input_value.right, Entry):
            return input_value.right.greaterThans(input_value.left)
        else:
            return True if input_value.left < input_value.right else False


class LessThanOrEqualsBinaryJudgeAlgorithm(Algorithm):
    def __init__(self):
        super(LessThanOrEqualsBinaryJudgeAlgorithm, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if isinstance(input_value.left, TimeSeries) or isinstance(input_value.left, Entry):
            return input_value.left.lessThanOrEquals(input_value.right)
        elif isinstance(input_value.right, TimeSeries) or isinstance(input_value.right, Entry):
            return input_value.right.greaterThanOrEquals(input_value.left)
        else:
            return True if input_value.left <= input_value.right else False


class ANDLogicBinaryJudgeAlgorithm(Algorithm):
    def __init__(self):
        super(ANDLogicBinaryJudgeAlgorithm, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if input_value.left and input_value.right:
            return True
        else:
            return False


class ORLogicBinaryJudgeAlgorithm(Algorithm):
    def __init__(self):
        super(ORLogicBinaryJudgeAlgorithm, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if input_value.left or input_value.right:
            return True
        else:
            return False


class XORLogicBinaryJudgeAlgorithm(Algorithm):
    def __init__(self):
        super(XORLogicBinaryJudgeAlgorithm, self).__init__(self.__class__.__name__)

    def _run_algorithm(self, input_value):
        if input_value.left and input_value.right:
            return False
        elif not input_value.left and not input_value.right:
            return False
        else:
            return True