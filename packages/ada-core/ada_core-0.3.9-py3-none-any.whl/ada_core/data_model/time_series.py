"""
Author: qiacai
"""

from collections import OrderedDict
from schematics.exceptions import ConversionError, BaseError, CompoundError
from collections import Mapping

from ada_core.data_model.entry import Entry


class TimeSeries(OrderedDict):

    def __init__(self, data: dict = None):
        super(TimeSeries, self).__init__()

        if data is not None:
            self.load_data(data)

    @property
    def start(self):
        """
        Return the earliest timestamp in the ts
        :return: int
        """
        return min(self.keys()) if self.keys() else None

    @property
    def end(self):
        """
        Return the latest timestamp in the ts
        :return: int
        """
        return max(self.keys()) if self.keys() else None

    def __repr__(self):
        return 'TimeSeries<start={0}, end={1}>'.format(repr(self.start), repr(self.end))

    def __str__(self):
        """
        :return string: Return string representation of time series
        """
        string_rep = ''
        for item in self.items():
            if not string_rep:
                string_rep += str(item)
            else:
                string_rep += ', ' + str(item)
        return 'TimeSeries([{}])'.format(string_rep)

    def getEntryList(self):
        entryList = []
        for key, value in self.items():
            entryList.append(Entry(key, value))
        return entryList

    def getValueList(self):
        return list(self.values())

    def getKeyList(self):
        return list(self.keys())

    def popEntry(self, key=None):
        if key is None:
            key = max(self.keys())
        entry = Entry(key, self.get(key))
        self.pop(key)
        return entry

    def split(self, key, direct=False):
        if key < 0 or key > max(self.keys()):
            return TimeSeries()

        ret_ts = {}
        keyList = list(self.keys())
        keyList = [keya for keya in keyList if keya>=key]
        for keya in keyList:
            ret_ts.update({keya:self.get(keya)})
            if direct:
                self.pop(keya)
        return TimeSeries(ret_ts)

    def load_data(self, value):

        if not isinstance(value, Mapping):
            raise ConversionError('Only mappings may be used to load TimeSeries')

        errors = {}
        for k in sorted(value.keys()):
            try:
                self.update({int(k): float(value.get(k))})
            except (BaseError, ValueError) as exc:
                errors[k] = exc
        if errors:
            raise CompoundError(errors)

    def equals(self, other):
        if not isinstance(other, TimeSeries):
            return False
        left_key_set = set(self.getKeyList())
        right_key_set = set(other.getKeyList())
        if len(left_key_set.difference(right_key_set)) > 0:
            return False
        for timestamp, value in self.items():
            if value != other.get(timestamp):
                return False
            else:
                continue
        return True

    def eq(self, other):
        output_value = TimeSeries()
        if isinstance(other, TimeSeries):
            left_key_set = set(self.getKeyList())
            right_key_set = set(other.getKeyList())
            if len(left_key_set.difference(right_key_set)) > 0:
                raise ValueError("Can only compare identically-labeled timeseries")
            for timestamp, value in self.items():
                output_value.update({timestamp: True if value == other.get(timestamp) else False})
        elif not (isinstance(other, int) or isinstance(other, float)):
            raise ValueError("Can only compare with numeric value or TimeSeries")
        else:
            for timestamp, value in self.items():
                output_value.update({timestamp: True if value == other else False})

        return output_value

    def __eq__(self, other):
        return self.eq(other)

    def gt(self, other):
        output_value = TimeSeries()
        if isinstance(other, TimeSeries):
            left_key_set = set(self.getKeyList())
            right_key_set = set(other.getKeyList())
            if len(left_key_set.difference(right_key_set)) > 0:
                raise ValueError("Can only compare identically-labeled timeseries")
            for timestamp, value in self.items():
                output_value.update({timestamp: True if value > other.get(timestamp) else False})
        elif not (isinstance(other, int) or isinstance(other, float)):
            raise ValueError("Can only compare with numeric value or TimeSeries")
        else:
            for timestamp, value in self.items():
                output_value.update({timestamp: True if value > other else False})

        return output_value

    def __gt__(self, other):
        return self.gt(other)

    def greaterThans(self, other):
        return True if sum(self.gt(other).getValueList()) >= len(other) else False

    def ge(self, other):
        output_value = TimeSeries()
        if isinstance(other, TimeSeries):
            left_key_set = set(self.getKeyList())
            right_key_set = set(other.getKeyList())
            if len(left_key_set.difference(right_key_set)) > 0:
                raise ValueError("Can only compare identically-labeled timeseries")
            for timestamp, value in self.items():
                output_value.update({timestamp: True if value >= other.get(timestamp) else False})
        elif not (isinstance(other, int) or isinstance(other, float)):
            raise ValueError("Can only compare with numeric value or TimeSeries")
        else:
            for timestamp, value in self.items():
                output_value.update({timestamp: True if value >= other else False})

        return output_value

    def __ge__(self, other):
        return self.ge(other)

    def greaterThanOrEquals(self, other):
        return True if sum(self.ge(other).getValueList()) >= len(other) else False

    def lt(self, other):
        output_value = TimeSeries()
        if isinstance(other, TimeSeries):
            left_key_set = set(self.getKeyList())
            right_key_set = set(other.getKeyList())
            if len(left_key_set.difference(right_key_set)) > 0:
                raise ValueError("Can only compare identically-labeled timeseries")
            for timestamp, value in self.items():
                output_value.update({timestamp: True if value < other.get(timestamp) else False})
        elif not (isinstance(other, int) or isinstance(other, float)):
            raise ValueError("Can only compare with numeric value or TimeSeries")
        else:
            for timestamp, value in self.items():
                output_value.update({timestamp: True if value < other else False})

        return output_value

    def __lt__(self, other):
        return self.lt(other)

    def lessThans(self, other):
        return True if sum(self.lt(other).getValueList()) >= len(other) else False

    def le(self, other):
        output_value = TimeSeries()
        if isinstance(other, TimeSeries):
            left_key_set = set(self.getKeyList())
            right_key_set = set(other.getKeyList())
            if len(left_key_set.difference(right_key_set)) > 0:
                raise ValueError("Can only compare identically-labeled timeseries")
            for timestamp, value in self.items():
                output_value.update({timestamp: True if value <= other.get(timestamp) else False})
        elif not (isinstance(other, int) or isinstance(other, float)):
            raise ValueError("Can only compare with numeric value or TimeSeries")
        else:
            for timestamp, value in self.items():
                output_value.update({timestamp: True if value <= other else False})

        return output_value

    def __le__(self, other):
        return self.le(other)

    def lessThanOrEquals(self, other):
        return True if sum(self.le(other).getValueList()) >= len(other) else False

    def _op_ts(self, other, op, fill_value):

        def run_op(a, b, op):
            if op in ['add', 'radd']:
                return a + b
            elif op == 'sub':
                return a - b
            elif op == 'rsub':
                return b - a
            elif op in ['mul', 'rmul']:
                return a * b
            elif op == 'truediv':
                return a / b
            elif op == 'rtruediv':
                return b / a
            elif op == 'floordiv':
                return a // b
            elif op == 'rfloordiv':
                return b // a
            elif op == 'mod':
                return a % b
            elif op == 'rmod':
                return b % a
            elif op == 'pow':
                return a ** b
            else:
                raise ValueError('unknown op')

        if not (isinstance(fill_value, int) or isinstance(fill_value, float)) and fill_value is not None:
            raise ValueError("fill_value should be numeric")

        output_value = TimeSeries()
        if isinstance(other, int) or isinstance(other, float):
            for timestamp, value in self.items():
                output_value.update({timestamp: run_op(value, other, op)})
            return output_value

        elif isinstance(other, TimeSeries):
            keyList = self.getKeyList() + other.getKeyList()
            keyList = sorted(list(set(keyList)))
            for key in keyList:
                value_left = self.get(key)
                value_right = other.get(key)
                if fill_value is None:
                    value_combine = run_op(value_left, value_right, op) if (value_left is not None and value_right is not None) else None
                else:
                    value_combine = run_op((value_left if value_left is not None else fill_value), (value_right if value_right is not None else fill_value), op)

                if value_combine is None:
                    continue
                else:
                    output_value.update({key: value_combine})
            return output_value
        else:
            raise ValueError("could only work with numeric value or TimeSeries")

    def add(self, other, fill_value=None):
        return self._op_ts(other, 'add',  fill_value)

    def __add__(self, other):
        return self.add(other)

    def radd(self, other, fill_value=None):
        return self._op_ts(other, 'radd',  fill_value)

    def __radd__(self, other):
        return self.radd(other)

    def sub(self, other, fill_value=None):
        return self._op_ts(other, 'sub',  fill_value)

    def __sub__(self, other):
        return self.sub(other)

    def rsub(self, other, fill_value=None):
        return self._op_ts(other, 'rsub',  fill_value)

    def __rsub__(self, other):
        return self.rsub(other)

    def mul(self, other, fill_value=None):
        return self._op_ts(other, 'mul',  fill_value)

    def __mul__(self, other):
        return self.mul(other)

    def rmul(self, other, fill_value=None):
        return self._op_ts(other, 'rmul',  fill_value)

    def __rmul__(self, other):
        return self.rmul(other)

    def truediv(self, other, fill_value=None):
        return self._op_ts(other, 'truediv',  fill_value)

    def __truediv__(self, other):
        return self.truediv(other)

    def rtruediv(self, other, fill_value=None):
        return self._op_ts(other, 'rtruediv',  fill_value)

    def __rtruediv__(self, other):
        return self.rtruediv(other)

    def floordiv(self, other, fill_value=None):
        return self._op_ts(other, 'floordiv',  fill_value)

    def __floordiv__(self, other):
        return self.floordiv(other)

    def rfloordiv(self, other, fill_value=None):
        return self._op_ts(other, 'rfloordiv',  fill_value)

    def __rfloordiv__(self, other):
        return self.rfloordiv(other)

    def mod(self, other, fill_value=None):
        return self._op_ts(other, 'mod',  fill_value)

    def __mod__(self, other):
        return self.mod(other)

    def rmod(self, other, fill_value=None):
        return self._op_ts(other, 'rmod',  fill_value)

    def __rmod__(self, other):
        return self.rmod(other)

    def pow(self, other, fill_value=None):
        return self._op_ts(other, 'pow',  fill_value)

    def __pow__(self, other):
        return self.pow(other)

    def __neg__(self):
        output_value = TimeSeries()
        for timestamp, value in self.items():
                output_value.update({timestamp: -value})
        return output_value

    def __pos__(self):
        output_value = TimeSeries()
        for timestamp, value in self.items():
                output_value.update({timestamp: +value})
        return output_value

    def __abs__(self):
        output_value = TimeSeries()
        for timestamp, value in self.items():
                output_value.update({timestamp: abs(value)})
        return output_value

    def __round__(self, n=None):
        output_value = TimeSeries()
        for timestamp, value in self.items():
                output_value.update({timestamp: round(value, n)})
        return output_value