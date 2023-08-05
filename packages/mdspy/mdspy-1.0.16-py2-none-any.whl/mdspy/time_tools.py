import datetime
from calendar import monthrange
from datetime import timedelta

import numpy as np
import pandas as pd
import time

epoch = pd.to_datetime(datetime.datetime.utcfromtimestamp(0)).tz_localize(tz='utc').to_pydatetime()


def to_tz(dt, tz='UTC'):
    try:
        return dt.tz_localize(tz)
    except:
        return dt.tz_convert(tz)


def unix_time_millis(dt):
    try:
        my_date = to_tz(dt).to_pydatetime()
    except:
        my_date = dt

    res = (my_date - epoch).total_seconds() * 1000.0
    return res


def add_month(dt0, n_months=1, dom=1):
    res = dt0.replace(day=1)
    for _ in range(n_months):
        res = res + timedelta(days=32)
        res = res.replace(day=1)
    min_days = np.min([dom, monthrange(res.year, res.month)[1]])
    res = res.replace(day=min_days)
    return res


def substract_month(dt0, n_months=1, dom=1):
    res = dt0.replace(day=1)
    for _ in range(n_months):
        res = res - timedelta(days=1)
        res = res.replace(day=1)

    min_days = np.min([dom, monthrange(res.year, res.month)[1]])
    res = res.replace(day=min_days)
    return res
