"""

Various Group by functions (based on dask to support not-fit-in-memory data)
 on files and dataframes

Author: Qu Tang

Date: 07/17/2018

"""
import os
import numpy as np
import pprint
import copy
import pandas as pd
from dask import delayed
from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler,\
    visualize
import dask
import itertools
from functools import reduce


class GroupBy:
    def __init__(self, data_inputs, **meta_infos):
        self._data_inputs = data_inputs
        self._meta_infos = meta_infos
        self._groups = {}
        self._groups_in_apply = {}

    @staticmethod
    def get_group_data(group):
        new_group_items = copy.deepcopy(group)
        new_group_items = [group_item['data']
                           for group_item in new_group_items]
        return new_group_items

    @staticmethod
    def get_group_metas(group):
        new_group_items = copy.deepcopy(group)
        group_metas = {}
        for group_item in new_group_items:
            metas = GroupBy.get_meta(group_item)
            for meta_name in metas:
                if meta_name in group_metas:
                    group_metas[meta_name].append(metas[meta_name])
                else:
                    group_metas[meta_name] = [metas[meta_name]]
        return group_metas

    @staticmethod
    def get_data_groups(groups):
        new_groups = copy.deepcopy(groups)
        for group_name in new_groups:
            new_groups[group_name] = GroupBy.get_group_data(
                new_groups[group_name])
        return new_groups

    @staticmethod
    def get_meta_groups(groups):
        new_groups = copy.deepcopy(groups)
        for group_name in new_groups:
            new_groups[group_name] = GroupBy.get_group_metas(
                new_groups[group_name])
        return new_groups

    @staticmethod
    def get_meta(group_item):
        new_group_item = copy.deepcopy(group_item)
        del new_group_item['data']
        return new_group_item

    @staticmethod
    def get_data(group_item):
        new_group_item = copy.deepcopy(group_item)
        return new_group_item['data']

    @staticmethod
    def bundle(data, **metas):
        bundle = {
            'data': data
        }
        for meta_name in metas:
            bundle[meta_name] = metas[meta_name]
        return bundle

    @staticmethod
    def get_adjacent_item(group_item, group):
        before_index = group_item['index'] - 1
        before_item = GroupBy.bundle(
            None) if before_index < 0 else group[before_index]
        after_index = group_item['index'] + 1
        after_item = GroupBy.bundle(None) if after_index >= len(
            group) else group[after_index]
        return before_item, after_item

    def _bundle_input(self):
        metas = self._meta_infos
        self._bundle_inputs = []
        for index, data in enumerate(self._data_inputs):
            bundle = {
                'data': data
            }
            for meta_name in metas:
                bundle[meta_name] = metas[meta_name][index]
            self._bundle_inputs.append(bundle)

    def _assign_to_groups(self, *groups):
        zipped_groups = list(zip(self._bundle_inputs, *groups))

        # assign to groups
        for zipped_group in zipped_groups:
            bundle_input = zipped_group[0]
            groups = zipped_group[1:]
            groups = filter(lambda x: x is not None, groups)
            group_name = '-'.join(groups)
            if group_name in self._groups:
                self._groups[group_name].append(bundle_input)
            else:
                self._groups[group_name] = [bundle_input]

    def _sort_in_groups(self, ingroup_sortkey_func=None, descending=False):
        # sort items in each group
        for group_name in self._groups:
            if ingroup_sortkey_func is None:
                self._groups[group_name].sort()
            else:
                self._groups[group_name].sort(
                    key=ingroup_sortkey_func, reverse=descending)

    def split(self, *groups, group_types=None, ingroup_sortkey_func=None, descending=False):
        """

        Group input by list of groups. Length should match the length of input
         list
        Results will be in a dictionary

        """

        self._bundle_input()

        self._assign_to_groups(*groups)

        self._sort_in_groups(
            ingroup_sortkey_func=ingroup_sortkey_func, descending=descending)

        self._groups_in_apply = copy.deepcopy(self._groups)

        self._group_types = group_types

        return self

    def post_join(self, join_func=None):
        for group_name in self._groups_in_apply:
            if join_func is not None:
                self._groups_in_apply[group_name] = [
                    join_func(self._groups_in_apply[group_name])]
        return self

    def final_join(self, join_func=None):
        self._joined_applied_groups = join_func(self._groups_in_apply, self._group_types)
        return self

    def compute_intermediate(self, **kwargs):
        self._groups_in_apply = dask.compute(
            self._groups_in_apply, **kwargs)[0]
        return self

    def compute(self, profiling=True, **kwargs):
        if profiling:
            with Profiler() as self._prof, \
                    ResourceProfiler(dt=0.25) as self._rprof, \
                    CacheProfiler() as self._cprof:
                self._result = dask.compute(
                    self._joined_applied_groups, **kwargs)[0]
        else:
            self._result = dask.compute(
                self._joined_applied_groups, **kwargs)[0]
        return self

    def show_profiling(self, **kwargs):
        visualize([self._prof, self._cprof, self._rprof], **kwargs)
        return self

    def visualize_workflow(self, **kwargs):
        dask.visualize(self._joined_applied_groups, **kwargs)

    def get_intermediate_result(self):
        return self._groups_in_apply

    def get_result(self):
        return self._result

    def print_groups(self):
        pprint.pprint(self._groups, width=1)

    def get_groups(self):
        return copy.deepcopy(self._groups)

    def apply(self, func, **kwargs):
        """[summary]

        Arguments:
            func {[type]} -- [description]
        """

        for group_name in self._groups_in_apply:
            results = []
            for index, group_item in \
                    enumerate(self._groups_in_apply[group_name]):
                group_item['index'] = index
                result = func(
                    group_item, self._groups_in_apply[group_name], **kwargs)
                results.append(result)
            self._groups_in_apply[group_name] = results
        return self


class GroupByWindowing(GroupBy):
    def __init__(self, *data_inputs, left_boundary, right_boundary):
        super(GroupByWindowing, self).__init__(*data_inputs)
        self._data_inputs = zip(
            self._data_inputs, left_boundary, right_boundary)

    def split_by_windowing(self, windowing_func, interval, step):
        def apply_windowing_func(data):
            start_windows = pd.date_range(
                start=data[1], end=data[2], freq=str(step) + 'S')
            stop_windows = start_windows + pd.Timedelta(interval, unit='s')
            stop_windows = stop_windows
            results = []
            for start_window, stop_window in zip(start_windows, stop_windows):
                chunk_result = windowing_func(
                    data[0], start_window, stop_window)
                results.append((chunk_result, start_window, stop_window))
            return results
        for group_name in self._groups:
            self._groups_in_apply[group_name] = [apply_windowing_func(
                group_item)
                for group_item in self._groups_in_apply[group_name]]
            self._groups_in_apply[group_name] = list(
                reduce((lambda a, b: a + b),
                       self._groups_in_apply[group_name]))
        return self

    def _assign_to_groups(self, *groups):
        zipped_groups = list(zip(self._data_inputs, *groups))

        # assign to groups
        for zipped_group in zipped_groups:
            data_input = zipped_group[0]
            groups = zipped_group[1:]
            group_name = '-'.join(groups)
            if group_name in self._groups:
                self._groups[group_name].append(data_input)
            else:
                self._groups[group_name] = [data_input]

    def apply(self, func, **kwargs):
        """[summary]

        Arguments:
            func {[type]} -- [description]
        """

        for group_name in self._groups:
            self._groups_in_apply[group_name] = [(func(
                group_item, self._groups[group_name], **kwargs),
                group_item[1], group_item[2])
                for group_item in self._groups_in_apply[group_name]]
        return self
