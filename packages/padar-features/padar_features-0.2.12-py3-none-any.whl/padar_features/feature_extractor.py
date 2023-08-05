"""

Feature extractor top-level interface

"""
from dask import delayed
from padar_parallel.groupby import GroupBy
from padar_parallel.grouper import MHealthGrouper
from padar_parallel.windowing import MhealthWindowing
from padar_converter.mhealth import dataset, fileio
import pandas as pd


class FeatureExtractor:
    def __init__(self):
        self._feature_set = None
        self._groupby = None
        self._grouper = None

    def add_feature_set(self, feature_set):
        self._feature_set = feature_set

    def extract_mhealth(self, data_inputs, interval=12.8, step=12.8,
                        scheduler='processes', **kwargs):
        compute = self._feature_set

        def sort_func(item):
            return dataset.get_file_timestamp(GroupBy.get_data(item))

        def load_data(item, all_items):
            metas = GroupBy.get_meta(item)
            data_loader = delayed(fileio.load_sensor)
            return GroupBy.bundle(data_loader(GroupBy.get_data(item)), **metas)

        @delayed
        def join_as_dataframe(groups):
            group_dfs = []
            groups = GroupBy.get_data_groups(groups)
            for group_name in groups:
                group_names = group_name.split('-')
                group_df = pd.concat(groups[group_name])
                group_col_names = []
                for name in group_names:
                    group_col_names.append('GROUP' +
                                           str(group_names.index(name)))
                    group_df['GROUP' +
                             str(group_names.index(name))] = name
                group_dfs.append(group_df)
            result = pd.concat(group_dfs, sort=False)
            result.set_index(group_col_names, inplace=True, append=True)
            return result

        @delayed
        @MhealthWindowing.groupby_windowing('sensor')
        def compute_features(df, **kwargs):
            return compute(df.values, **kwargs)

        self._inputs = data_inputs
        self._grouper = MHealthGrouper(data_inputs)
        self._groupby = GroupBy(
            data_inputs, **MhealthWindowing.make_metas(data_inputs))
        groups = [
            self._grouper.pid_group(),
            self._grouper.sid_group(),
            self._grouper.auto_init_placement_group()
        ]
        self._groupby.split(*groups,
                            ingroup_sortkey_func=sort_func,
                            descending=False)
        self._groupby.apply(load_data)
        self._groupby.apply(
            compute_features, interval=interval, step=step, **kwargs)
        self._groupby.final_join(join_as_dataframe)
        self._result = self._groupby.compute(
            scheduler=scheduler, **kwargs).get_result()
        return self

    def show_profiling(self):
        self._groupby.show_profiling()

    def save(self, filepath):
        self._result.to_csv(filepath, float_format='%.9f', index=True)


if __name__ == '__main__':
    from clize import run
    from padar_features.feature_set import FeatureSet
    from glob import glob
    extractor = FeatureExtractor()
    extractor.add_feature_set(FeatureSet.compute_posture_and_activity)

    def extract_features(file_pattern, *, output,
                         interval=12.8, step=12.8, sr):
        files = glob(file_pattern, recursive=True)
        extractor.extract_mhealth(
            files, scheduler='processes', interval=interval, step=step,
            sr=int(sr))
        extractor.show_profiling()
        extractor.save(output)

    # extract_features('D:/data/spades_lab/SPADES_2/MasterSynced/**/Actigraph*.sensor.csv',
    #  output='./test.csv', sr=80)
    run(extract_features)
