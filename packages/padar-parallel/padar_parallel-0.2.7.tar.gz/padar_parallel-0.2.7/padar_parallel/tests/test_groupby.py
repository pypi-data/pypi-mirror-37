from ..grouper import MHealthGrouper
from ..groupby import GroupBy
from padar_converter.mhealth import dataset
import numpy as np

test_file_list = [
    "./SPADES_1/MasterSynced/2015/09/24/14/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150066-AccelerationCalibrated.2015-09-24-14-23-00-000-M0400.sensor.csv",
    "./SPADES_1/MasterSynced/2015/09/24/16/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150175-AccelerationCalibrated.2015-09-24-16-00-00-000-M0400.sensor.csv",
    "./SPADES_10/MasterSynced/2015/12/07/18/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150066-AccelerationCalibrated.2015-12-07-18-00-00-000-M0500.sensor.csv",
    "./SPADES_10/MasterSynced/2015/12/07/19/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150075-AccelerationCalibrated.2015-12-07-18-00-00-000-M0500.sensor.csv",
    "./SPADES_11/MasterSynced/2015/12/11/17/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150075-AccelerationCalibrated.2015-12-11-17-00-00-000-M0500.sensor.csv",
    "./SPADES_11/MasterSynced/2015/12/11/18/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150084-AccelerationCalibrated.2015-12-11-17-00-00-000-M0500.sensor.csv",
    "./SPADES_12/MasterSynced/2015/12/14/11/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150075-AccelerationCalibrated.2015-12-14-11-15-00-000-M0500.sensor.csv",
    "./SPADES_12/MasterSynced/2015/12/15/11/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150084-AccelerationCalibrated.2015-12-14-11-15-00-000-M0500.sensor.csv"
]


def test_groupby_split():
    groupby_obj = GroupBy(*test_file_list)
    grouper = MHealthGrouper(test_file_list)
    groupby_obj = groupby_obj.split(grouper.pid_group(
    ), ingroup_sortkey_func=dataset.get_file_timestamp, descending=True)
    gt_dict = {'SPADES_1': ['./SPADES_1/MasterSynced/2015/09/24/16/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150175-AccelerationCalibrated.2015-09-24-16-00-00-000-M0400.sensor.csv',
                            './SPADES_1/MasterSynced/2015/09/24/14/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150066-AccelerationCalibrated.2015-09-24-14-23-00-000-M0400.sensor.csv'],
               'SPADES_10': ['./SPADES_10/MasterSynced/2015/12/07/18/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150066-AccelerationCalibrated.2015-12-07-18-00-00-000-M0500.sensor.csv',
                             './SPADES_10/MasterSynced/2015/12/07/19/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150075-AccelerationCalibrated.2015-12-07-18-00-00-000-M0500.sensor.csv'],
               'SPADES_11': ['./SPADES_11/MasterSynced/2015/12/11/17/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150075-AccelerationCalibrated.2015-12-11-17-00-00-000-M0500.sensor.csv',
                             './SPADES_11/MasterSynced/2015/12/11/18/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150084-AccelerationCalibrated.2015-12-11-17-00-00-000-M0500.sensor.csv'],
               'SPADES_12': ['./SPADES_12/MasterSynced/2015/12/14/11/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150075-AccelerationCalibrated.2015-12-14-11-15-00-000-M0500.sensor.csv',
                             './SPADES_12/MasterSynced/2015/12/15/11/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150084-AccelerationCalibrated.2015-12-14-11-15-00-000-M0500.sensor.csv']}
    assert groupby_obj._groups == gt_dict
