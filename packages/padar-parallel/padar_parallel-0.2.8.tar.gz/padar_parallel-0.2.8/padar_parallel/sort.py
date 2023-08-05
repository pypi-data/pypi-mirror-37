from padar_converter.mhealth import dataset
from .groupby import GroupBy


def sort_by_file_timestamp(item):
    return dataset.get_file_timestamp(GroupBy.get_data(item))
