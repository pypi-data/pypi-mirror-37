import numpy as np
import pandas as pd

from mdspy.PCA_timeseries import ts_pca, create_sliding_windows


def feature_creators(list_functions, history_size, big_data=False):
    def feats_and_concat(small_df):
        small_df.index = small_df.index.get_level_values(0)
        index = small_df.index[-1]
        line = pd.DataFrame()
        for func in list_functions:
            tmp = func(small_df)
            line = pd.concat([line, tmp], axis=1)
        line.index = [index]
        feature_creators.res = pd.concat([feature_creators.res, line], axis=0)

    def run(df):
        feature_creators.res = pd.DataFrame()
        # df = df.reset_index(drop=True)

        if big_data:
            for i in range(len(df.index) - history_size + 1):
                sub_df = df[i:i + history_size]
                feats_and_concat(sub_df)
        else:
            _roll(df, history_size=history_size).apply(feats_and_concat)
        return feature_creators.res

    return run


def fe_get_day_of_week(name_of_feature):
    def get_day_of_week(df_small):
        return pd.DataFrame({name_of_feature: [df_small.index[-1].weekday()]})

    return get_day_of_week


def fe_get_lag(name_of_feature, target, lag=1):
    def get_lag(df_small):
        return pd.DataFrame({name_of_feature: [df_small[target].shift(lag).values[-1]]})

    return get_lag


def fe_get_diff(name_of_feature, target, jump=2):
    def get_diff(df_small):
        return pd.DataFrame({name_of_feature: [df_small[target].diff(jump).values[-1]]})

    return get_diff


def fe_get_pca(name_of_feature, target, nb_component, df, windows_size):
    df = create_sliding_windows(df, target, windows_size)
    pca = ts_pca(df.reset_index(drop=True), n_components=nb_component)

    def get_pca(df_small):
        df_small_windows = create_sliding_windows(df_small, target, windows_size)
        df_with_pca = pca.transform(df_small_windows)
        data_dict = {}
        for i in range(nb_component):
            data_dict[name_of_feature + '_' + str(i + 1)] = [df_with_pca['PCA' + '_' + str(i + 1)].values[-1]]

        res = pd.DataFrame(data_dict)

        return res

    return get_pca


def _roll(df, history_size, **kwargs):
    df = df.dropna(axis=0)
    roll_array = np.dstack([df.values[i:i + history_size, :] for i in range(len(df.index) - history_size + 1)]).T
    panel = pd.Panel(roll_array,
                     items=df.index[history_size - 1:],
                     major_axis=df.columns, minor_axis=pd.Index(range(history_size), name='roll'))
    df_group = panel.to_frame().unstack().T.groupby(level=0, **kwargs)
    return df_group
