# -*- coding: utf-8 -*-


import unittest

import pandas as pd

from mdspy import analytics


class AnalyticsTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_correlation(self):
        t_correlation = analytics.correlation([1.0, 2.0, 2.0], [1.0, 2.0, 2.0])
        self.assertEqual(t_correlation['pearson_correlation_coefficient'], 1.0)
        self.assertEqual(t_correlation['interpretation'], 'Strong positive correlation')

    def test_clustering_density(self):
        dataset = [[1, 1], [1, 2], [1, 2], [5, 10], [2, 10]]
        df_clustering = pd.DataFrame(dataset)
        df_clustering.columns = ['col1', 'col2']
        t_clustering = analytics.clustering_density(df_clustering, ['col1', 'col2'], 2, 4, 50, 42)
        self.assertEqual(t_clustering['clusters'], [1, 1, 1, 0, 0])
        self.assertEqual(t_clustering['cluster_distribution'], {1: 3, 0: 2})
        self.assertAlmostEqual(t_clustering['centroids'], [[3.5, 10.0], [1.0, 1.6666666666666665]])
        self.assertAlmostEqual(t_clustering['sum_intra_cluster_distances'], 5.1666666666666661)
        self.assertAlmostEqual(t_clustering['sum_inter_cluster_distances'], 75.694444444444443)

    def test_clustering_hierarchical(self):
        dataset = [[1, 1], [1, 2], [1, 2], [5, 10], [2, 10]]
        df_clustering = pd.DataFrame(dataset)
        df_clustering.columns = ['col1', 'col2']
        t_clustering = analytics.clustering_hierarchical(df_clustering, ['col1', 'col2'], 2)
        # print (t_clustering)
        self.assertEqual(t_clustering['clusters'], [1, 1, 1, 2, 2])
        self.assertEqual(t_clustering['cluster_distribution'], {1: 3, 2: 2})
        self.assertAlmostEqual(t_clustering['centroids'], [[1.0, 1.6666666666666667], [3.5, 10.0]])
        self.assertAlmostEqual(t_clustering['sum_intra_cluster_distances'], 5.1666666666666661)
        self.assertAlmostEqual(t_clustering['sum_inter_cluster_distances'], 75.694444444444443)


if __name__ == '__main__':
    unittest.main()
