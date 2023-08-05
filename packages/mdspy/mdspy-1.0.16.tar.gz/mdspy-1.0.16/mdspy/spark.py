import sys
from os import environ

import pandas as pd
from pyspark import SparkContext, SparkConf


def init_spark(nb_cores='*'):
    python_exec = sys.executable

    environ['PYSPARK_PYTHON'] = python_exec
    environ['PYSPARK_DRIVER_PYTHON'] = python_exec
    environ['SPARK_YARN_USER_ENV'] = python_exec
    conf = SparkConf().setAppName("App")

    conf = (conf.setMaster('local[' + str(nb_cores) + ']')
            .set('spark.executor.memory', '4G')
            .set('spark.driver.memory', '45G')
            .set('spark.driver.maxResultSize', '10G'))
    sc = SparkContext(conf=conf)
    j_log = sc._jvm.org.apache.log4j
    j_log.LogManager.getRootLogger().setLevel(j_log.Level.OFF)
    return sc


def run_spark_job_concat_dfs(parameters_list, function_to_parallelize, nb_cores='*', sc=None):
    """
    This function should be used when the goal is to parallelilze a job across many parameters.
    The results are then concatenated into an dataframe
    Parameters to define:
    1. parameter_list: a list of the sets of arguments necessary to run the function to parallelize
    2. function to paralelize: function that must return an object to concatenate (most likely a dataframe). Its required arguments should be included in the parameter_list
    Default parameter:
    3. nb_cores: '*' is the default value meaning if not specified it will use all cores available.
    This function returns a concatenate dataframe
    """
    if sc is None:
        sc = init_spark(nb_cores)
    rdd = sc.parallelize(parameters_list)
    results = rdd.map(function_to_parallelize).reduce(lambda a, b: pd.concat([a, b], axis=0))
    return results


def run_spark_job_no_reduce(parameters_list, function_to_parallelize, nb_cores='*', sc=None):
    """
    This function should be used when the goal is to parallelilze a job across many parameters.
    The results are not reduced
    Parameters to define:
    1. parameter_list: a list of the sets of arguments necessary to run the function to parallelize
    2. function to paralelize: function that must return an object to concatenate (most likely a dataframe). Its required arguments should be included in the parameter_list
    Default parameter:
    3. nb_cores: '*' is the default value meaning if not specified it will use all cores available.
    This function returns a concatenate dataframe
    """
    if sc is None:
        sc = init_spark(nb_cores)
    rdd = sc.parallelize(parameters_list)
    rdd.map(function_to_parallelize).collect()
