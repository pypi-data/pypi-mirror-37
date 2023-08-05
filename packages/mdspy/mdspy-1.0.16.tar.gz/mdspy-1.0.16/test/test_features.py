# -*- coding: utf-8 -*-

import unittest

from mdspy.data_creation import create_simple_data
from mdspy.features import fe_get_day_of_week, feature_creators, fe_get_lag, fe_get_diff


class Features_test(unittest.TestCase):
    """Basic test cases."""

    def test_feature_day_of_week(self):
        df = create_simple_data(10, 50, 0, timeseries=True)
        func_dow = fe_get_day_of_week('dow')
        run = feature_creators([func_dow], history_size=2)
        res = run(df)
        print(res)
        expected_shape = (9, 1)
        actual_shape = res.shape
        self.assertEqual(expected_shape, actual_shape)
        self.assertEqual(28, res['dow'].sum())

    def test_lag(self):
        df = create_simple_data(10, 50, 0, timeseries=True)
        print('here df', df)
        func_dow = fe_get_lag('col_num1_lag_1', 'col_num1', lag=1)
        run = feature_creators([func_dow], history_size=4)
        res = run(df)
        print('here res', res)
        res.to_csv('check_this_out.csv')
        expected_shape = (7, 1)
        actual_shape = res.shape
        self.assertEqual(expected_shape, actual_shape)
        self.assertEqual(35, res['col_num1_lag_1'].sum())

    def test_diff(self):
        df = create_simple_data(10, 50, 0, timeseries=True)
        print('here df', df)
        func_dow = fe_get_diff('col_num1_lag_1', 'col_num1', jump=2)
        run = feature_creators([func_dow], history_size=4)
        res = run(df)
        print('here res', res)
        res.to_csv('check_this_out.csv')
        expected_shape = (7, 1)
        actual_shape = res.shape
        self.assertEqual(expected_shape, actual_shape)
        self.assertEqual(14, res['col_num1_lag_1'].sum())
