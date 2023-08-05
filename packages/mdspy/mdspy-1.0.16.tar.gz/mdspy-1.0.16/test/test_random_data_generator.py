# -*- coding: utf-8 -*-

import unittest

import pandas as pd

from mdspy.data_creation import create_random_normal_data


class Spark_test(unittest.TestCase):
    """Basic test cases."""

    def test_random_data(self):
        # Testing case with both kinds of columns
        df = create_random_normal_data(10, 3, 5, 6, 4)
        expected_len = 10
        actual_len = len(df)
        expected_width = 7
        actual_width = len(df.columns)
        self.assertEqual(expected_len, actual_len)
        self.assertEqual(expected_width, actual_width)

        # Testing case with no num columns
        df2 = create_random_normal_data(10, 0, 5, 6, 4)
        expected_len = 10
        actual_len = len(df2)
        expected_width = 4
        actual_width = len(df2.columns)

        self.assertEqual(expected_len, actual_len)
        self.assertEqual(expected_width, actual_width)

        # Testing case no cat columns

        df2 = create_random_normal_data(10, 3, 5, 6, 0)
        expected_len = 10
        actual_len = len(df2)
        expected_width = 3
        actual_width = len(df2.columns)

        self.assertEqual(expected_len, actual_len)
        self.assertEqual(expected_width, actual_width)

    def test_random_timeseries_data(self):
        # Testing case with both kinds of columns
        df = create_random_normal_data(10, 3, 5, 6, 4, timeseries=True)
        expected_datetime_value_type = type(pd.to_datetime('2018-01-01'))
        actual_datetime_value_type = type(df.index[0])

        self.assertEqual(expected_datetime_value_type, actual_datetime_value_type)
