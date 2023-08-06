"""
Author: qiacai
"""
from numbers import Number
import numpy as np

from ada_core import exceptions, utils, constants
from ada_core.algorithms import Algorithm
from ada_core.data_model.io_data_type import AlgorithmIODataType
from ada_core.data_model.time_series import TimeSeries
from ada_core.data_model.entry import Entry


class Scale(Algorithm):

    def __init__(self):
        super(Scale, self).__init__(self.__class__.__name__)
        # self.name = 'value_scale'

    def _run_algorithm(self, input_value, operator):

        if type(input_value) == AlgorithmIODataType.ENTRY.value.native_type:
            input_value = TimeSeries({input_value.timestamp, input_value.value})

        output_value = TimeSeries()
        if operator == "*":
            for timestamp, value in input_value.right.items():
                output_value.update({timestamp: (value * input_value.left)})
        elif operator == "/":
            for timestamp, value in input_value.right.items():
                output_value.update({timestamp: (value / input_value.left)})
        elif operator == "+":
            for timestamp, value in input_value.right.items():
                output_value.update({timestamp: (value + input_value.left)})
        elif operator == "-":
            for timestamp, value in input_value.right.items():
                output_value.update({timestamp: (value - input_value.left)})
        else:
            raise exceptions.ParametersNotPassed("The input operator should be in ['*', '/', '+', '-']")

        if type(input_value) == AlgorithmIODataType.ENTRY.value.native_type:
            output_value = Entry(output_value.getKeyList()[0], output_value.getValueList()[0])

        return output_value

# value_scale

# value_compare