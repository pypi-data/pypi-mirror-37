import functools
from padar_converter.mhealth import dataset, dataframe, fileio
from padar_converter import utils
import pandas as pd
from .groupby import GroupBy
from .grouper import MHealthGrouper


class MhealthWindowing:
    @staticmethod
    def make_metas(inputs):
        grouper = MHealthGrouper(inputs)
        return {
            'left_boundary': grouper.session_start_time(),
            'right_boundary': grouper.session_stop_time()
        }

    def get_segment_func(file_type):
        if file_type == 'sensor':
            return dataframe.segment_sensor
        elif file_type == 'annotation':
            return dataframe.segment_annotation

    def get_load_func(file_type):
        if file_type == 'sensor':
            return fileio.load_sensor
        elif file_type == 'annotation':
            return fileio.load_annotation

    def get_times(df, file_type):
        if file_type == 'sensor':
            return dataframe.start_time(df), dataframe.end_time(df)
        elif file_type == 'annotation':
            return dataframe.start_time(df, start_time_col=1), \
                dataframe.end_time(df, stop_time_col=2)

    def get_segment_windows(lbound, rbound, interval, step):
        start_windows = pd.date_range(
            start=lbound, end=rbound, freq=str(step) + 'S')
        stop_windows = start_windows + \
            pd.Timedelta(interval, unit='s')
        return start_windows, stop_windows

    @staticmethod
    def groupby_windowing(file_type):
        segment_func = MhealthWindowing.get_segment_func(file_type)

        def wrapper(func):
            def groupby_windowing_func(data, all_data, interval, step,
                                       **kwargs):

                original_data = GroupBy.get_data(data)
                before_item, after_item = GroupBy.get_adjacent_item(
                    data, all_data)
                before_data = GroupBy.get_data(before_item)

                original_st, original_et = MhealthWindowing.get_times(
                    original_data, file_type)

                appended_data = dataframe.append_edges(
                    original_data, before_df=before_data, after_df=None,
                    duration=interval * 5)

                start_windows, stop_windows = MhealthWindowing.get_segment_windows(
                    data['left_boundary'], data['right_boundary'],
                    interval, step)

                rest_metas = GroupBy.get_meta(data)

                results = []
                for start_window, stop_window in \
                        zip(start_windows, stop_windows):

                    if stop_window <= original_st or \
                            stop_window >= original_et:
                        continue

                    chunk_result = segment_func(
                        appended_data, start_window, stop_window)

                    result = func(chunk_result, interval=interval, step=step, **rest_metas, **kwargs)

                    result = dataframe.append_times(
                        result, start_window, stop_window)

                    results.append(result)
                return GroupBy.bundle(pd.concat(results))

            return groupby_windowing_func
        return wrapper

    @staticmethod
    def script_windowing(file_type):
        segment_func = MhealthWindowing.get_segment_func(file_type)
        load_func = MhealthWindowing.get_load_func(file_type)

        def wrapper(func):
            def script_windowing_func(file, *,
                                      before_file=None, lbound, rbound,
                                      interval, step, **kwargs):

                original_data = load_func(file)
                before_data = load_func(before_file)

                original_st, original_et = MhealthWindowing.get_times(
                    original_data, file_type)

                appended_data = dataframe.append_edges(
                    original_data, before_df=before_data, duration=interval * 5)

                start_windows, stop_windows = MhealthWindowing.get_segment_windows(
                    lbound, rbound, interval, step)

                results = []
                for start_window, stop_window in \
                        zip(start_windows, stop_windows):

                    if stop_window <= original_st or \
                            stop_window >= original_et:
                        continue

                    chunk_result = segment_func(
                        appended_data, start_window, stop_window)

                    result = func(chunk_result, **kwargs)

                    result = dataframe.append_times(
                        result, start_window, stop_window)

                    results.append(result)
                return pd.concat(results)

            return script_windowing_func
        return wrapper
