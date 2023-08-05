import numpy as np
import pandas as pd


def create_random_normal_data(nb_rows, nb_numerical_col, mu, sigma, nb_categorical_col, timeseries=False):
    np.random.seed(42)
    cat_value = 'a'
    data = {}
    for i in range(nb_numerical_col):
        col_name = 'col_num' + str(i)
        data[col_name] = np.random.normal(mu, sigma, size=nb_rows)
    for j in range(nb_categorical_col):
        col_name = 'col_cat' + str(j)
        data[col_name] = [cat_value] * nb_rows
    df = pd.DataFrame(data)
    if timeseries:
        df = _transform_to_timeseries_data(df)
    return df


def create_simple_data(nb_rows, nb_numerical_col, nb_categorical_col, timeseries=False):
    np.random.seed(42)
    cat_value = 'a'
    data = {}
    for i in range(nb_numerical_col):
        col_name = 'col_num' + str(i)
        data[col_name] = range(0, nb_rows)
    for j in range(nb_categorical_col):
        col_name = 'col_cat' + str(j)
        data[col_name] = [cat_value] * nb_rows
    df = pd.DataFrame(data)
    if timeseries:
        df = _transform_to_timeseries_data(df)
    return df


def _transform_to_timeseries_data(df):
    start = pd.to_datetime('2018-08-08')
    rng = pd.date_range(start, periods=len(df))
    df['DateTime'] = rng

    ts = df.set_index('DateTime')
    ts.index = pd.to_datetime(ts.index)
    return ts
