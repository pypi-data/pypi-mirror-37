from .groupby import GroupBy
import pandas as pd


def join_as_dataframe(groups, group_types=None):
    group_dfs = []
    groups = GroupBy.get_data_groups(groups)
    for group_name in groups:
        group_names = group_name.split('-')
        group_df = pd.concat(groups[group_name])
        group_col_names = []
        for name in group_names:
            i = group_names.index(name)
            if group_types is None:
                group_col_name = 'GROUP' + str(i)
            else:
                group_col_name = group_types[i]
            group_col_names.append(group_col_name)
            group_df[group_col_name] = name
        group_dfs.append(group_df)
    result = pd.concat(group_dfs, sort=False)
    result.set_index(group_col_names, inplace=True, append=True)
    return result
