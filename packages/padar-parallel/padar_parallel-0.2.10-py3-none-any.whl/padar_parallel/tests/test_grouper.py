from ..grouper import MHealthGrouper
import numpy as np

test_file_list = [
"./SPADES_1/MasterSynced/2015/09/24/14/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150066-AccelerationCalibrated.2015-09-24-14-23-00-000-M0400.sensor.csv",
"./SPADES_1/MasterSynced/2015/09/24/16/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150175-AccelerationCalibrated.2015-09-24-16-00-00-000-M0400.sensor.csv",
"./SPADES_10/MasterSynced/2015/12/07/18/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150066-AccelerationCalibrated.2015-12-07-18-00-00-000-M0500.sensor.csv",
"./SPADES_10/MasterSynced/2015/12/07/18/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150075-AccelerationCalibrated.2015-12-07-18-00-00-000-M0500.sensor.csv",
"./SPADES_11/MasterSynced/2015/12/11/17/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150075-AccelerationCalibrated.2015-12-11-17-00-00-000-M0500.sensor.csv",
"./SPADES_11/MasterSynced/2015/12/11/17/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150084-AccelerationCalibrated.2015-12-11-17-00-00-000-M0500.sensor.csv",
"./SPADES_12/MasterSynced/2015/12/14/11/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150075-AccelerationCalibrated.2015-12-14-11-15-00-000-M0500.sensor.csv",
"./SPADES_12/MasterSynced/2015/12/14/11/ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150084-AccelerationCalibrated.2015-12-14-11-15-00-000-M0500.sensor.csv"
]

def test_mhealthgrouper():
    grouper = MHealthGrouper(test_file_list)
    pid_groups = grouper.pid_group()
    sid_groups = grouper.sid_group()
    file_type_groups = grouper.file_type_group()
    data_type_groups = grouper.data_type_group()
    sensor_type_groups = grouper.sensor_type_group()
    assert np.array_equal(np.array(pid_groups), np.array(['SPADES_1', 'SPADES_1', 'SPADES_10', 'SPADES_10', 'SPADES_11', 'SPADES_11', 'SPADES_12', 'SPADES_12']))
    assert np.array_equal(np.array(sid_groups), np.array(['TAS1E23150066', 'TAS1E23150175', 'TAS1E23150066', 'TAS1E23150075', 'TAS1E23150075', 'TAS1E23150084', 'TAS1E23150075', 'TAS1E23150084']))
    assert np.array_equal(np.array(file_type_groups), np.array(['sensor'] * len(sid_groups)))
    assert np.array_equal(np.array(data_type_groups), np.array(['AccelerationCalibrated'] * len(sid_groups)))
    assert np.array_equal(np.array(sensor_type_groups), np.array(['ActigraphGT9X'] * len(sid_groups)))


