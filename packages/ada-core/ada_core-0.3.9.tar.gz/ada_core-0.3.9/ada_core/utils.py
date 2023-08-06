"""
Author: qiacai
"""

from ada_core.data_model.time_series import TimeSeries
from ada_core.data_model.entry import Entry
from datetime import timedelta, datetime
import pytz
from dateutil.relativedelta import relativedelta
import numpy as np
from ada_core import constants


# def isfloat(x):
#     try:
#         float(x)
#         return True
#     except ValueError or TypeError:
#         return False


# def isbool(x):
#     try:
#         strValue = str(x)
#         if strValue.lower() in ("true", "yes", "t", "1", "y", "false", "no", "f", "0", "n"):
#             return True
#         else:
#             return False
#     except ValueError or TypeError:
#         return False


# def str2bool(x):
#     if isbool(x):
#         return str(x).lower() in ("true", "yes", "t", "1", "y")
#     else:
#         return False


# def isSimpleValue(x):
#     try:
#         if isinstance(x, Entry) or isinstance(x, TimeSeries) or isbool(x) or isfloat(x) or str.isdecimal(str(x)):
#             return True
#         else:
#             return False
#     except TypeError or ValueError:
#         return False


def window2timestamp(ts, window, timezone=None):

    if timezone is None:
        timezone = constants.ALGORITHM_DEFAULT_TIMEZONE

    window_str = str(window)
    end_str = window_str[-1]
    if end_str in ['s', 'm', 'h', 'd', 'w', 'M', 'y']:
        try:
            num = abs(int(window[:-1]))
            if num == 0:
                return ts.getKeyList()[-1]
        except RuntimeError:
            raise ValueError('input ts or window is not valid')
        time_stamp = datetime.fromtimestamp(ts.end, tz=pytz.timezone(timezone))
        if end_str == 's':
             time_stamp = time_stamp+relativedelta(seconds=-num)
        elif end_str =='m':
            time_stamp = time_stamp+relativedelta(minutes=-num)
        elif end_str=='h':
            time_stamp = time_stamp+relativedelta(hours=-num)
        elif end_str=='d':
            time_stamp = time_stamp+relativedelta(days=-num)
        elif end_str=='w':
            time_stamp = time_stamp+relativedelta(weeks=-num)
        elif end_str=='M':
            time_stamp = time_stamp+relativedelta(months=-num)
        else: #end_str=='y':
            time_stamp = time_stamp+relativedelta(years=-num)

        return int(time_stamp.timestamp())

    else:
        try:
            num = abs(int(window_str))
            if num == 0:
                num = 1
        except RuntimeError:
            raise ValueError('input window is not valid')

        if len(ts) < num:
            raise ValueError('the timeseries is not long enough')
        else:
            return ts.getKeyList()[-(num)]

