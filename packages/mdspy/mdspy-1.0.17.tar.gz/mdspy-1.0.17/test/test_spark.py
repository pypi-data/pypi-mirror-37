# -*- coding: utf-8 -*-

import unittest

from mdspy.data_creation import create_random_normal_data
from mdspy.spark import run_spark_job_concat_dfs, run_spark_job_no_reduce, init_spark


class Spark_test(unittest.TestCase):
    """Basic test cases."""

    @classmethod
    def setUpClass(cls):
        print('i am here')
        cls.sc = init_spark()

    def test_spark_concat_dfs(self):
        # df = pd.read_csv('../data/energydata_complete.csv')
        df = create_random_normal_data(10, 2, 3, 4, 5)
        parameters = [df.head(10), df.tail(10)]
        parameters_devices = [['dev1', 'dev2', 'dev3'], ['dev4', 'dev5', 'dev6']]

        def funct(df):
            return df.head(5)

        df_res = run_spark_job_concat_dfs(parameters, funct, nb_cores='*', sc=Spark_test.sc)
        expected = 10
        actual = len(df_res)
        self.assertEqual(expected, actual)

    def test_spark_no_reduce_dfs(self):
        # df = pd.read_csv('../data/energydata_complete.csv')
        df = create_random_normal_data(10, 2, 3, 4, 5)
        parameters = [df.head(10), df.tail(10)]
        parameters_devices = [['dev1', 'dev2', 'dev3'], ['dev4', 'dev5', 'dev6']]

        def funct(df):
            return df.head(5)

        run_spark_job_no_reduce(parameters, funct, nb_cores='*', sc=Spark_test.sc)

        self.assertTrue(True)

    @classmethod
    def tearDownClass(cls):
        cls.sc.stop()
