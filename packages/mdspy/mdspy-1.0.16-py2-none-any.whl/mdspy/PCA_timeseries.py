import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA


def create_sliding_windows(df, col_name, window_size):
    res = df.copy()
    for i in range(1, window_size + 1):
        res[col_name + '_' + str(i)] = res[col_name].shift(i)
        cols = [col_name] + [col_name + '_' + str(i) for i in range(1, window_size + 1)]
        cols.reverse()
    res = res[cols].dropna(axis=0)
    return res


class ts_pca:
    def __init__(self, df, n_components=3):
        self.pca = PCA(n_components=n_components)
        self.df = df
        self.pca.fit(df)
        self._projected = None

    def get_PCA(self):
        return self.pca

    def transform(self, df=None):
        col_names = ['PCA_' + str(i) for i in range(1, self.pca.n_components_ + 1)]
        if df is None:
            if self._projected is not None:
                return self._projected
            self._projected = pd.DataFrame(self.pca.transform(self.df), index=self.df.index, columns=col_names)

            return self._projected
        res = pd.DataFrame(self.pca.transform(df), index=df.index, columns=col_names)
        return res

    def get_report(self):
        return 'number of components: ' + str(self.pca.n_components) + '\n' + \
               'explained variance: ' + str(self.pca.explained_variance_ratio_)

    def plot_coefficients(self):
        fig, axs = plt.subplots(self.pca.n_components, 1, sharex=True)
        for i in range(self.pca.n_components):
            axs[i].bar(range(len(self.pca.components_[i])), self.pca.components_[i], label='PCA_' + str(i + 1))
        fig.subplots_adjust(hspace=0)
        plt.show()

    def inverse_transform(self):
        if self._projected is None:
            self.transform()
        return pd.DataFrame(self.pca.inverse_transform(self._projected), index=self._projected.index,
                            columns=self.df.columns)
