from padar_converter.mhealth import dataset
from functools import partial


class Grouper:
    def __init__(self, data_inputs):
        self._data_inputs = data_inputs

    def get_group(self, grouping_func):
        return grouping_func(self._data_inputs)


class MHealthGrouper(Grouper):
    def pid_group(self):
        return self.get_group(
            lambda inputs: list(
                map(dataset.get_pid, inputs)
            )
        )

    def session_start_time(self):
        return self.get_group(
            lambda inputs: list(
                map(partial(dataset.get_session_start_time,
                            filepaths=inputs), inputs)
            )
        )

    def session_stop_time(self):
        return self.get_group(
            lambda inputs: list(
                map(partial(dataset.get_session_end_time,
                            filepaths=inputs), inputs)
            )
        )

    def get_init_placement_group(self, mapping_file):
        return self.get_group(
            lambda inputs: list(
                map(partial(dataset.get_init_placement,
                            mapping_file=mapping_file), inputs)
            )
        )

    def auto_init_placement_group(self):
        return self.get_group(
            lambda inputs: list(
                map(dataset.auto_init_placement, inputs)
            )
        )

    def sid_group(self):
        return self.get_group(
            lambda inputs: list(
                map(dataset.get_sid, inputs)
            )
        )

    def annotator_group(self):
        return self.get_group(
            lambda inputs: list(
                map(dataset.get_sid, inputs)
            )
        )

    def sensor_type_group(self):
        return self.get_group(
            lambda inputs: list(
                map(dataset.get_sensor_type, inputs)
            )
        )

    def file_type_group(self):
        return self.get_group(
            lambda inputs: list(
                map(dataset.get_file_type, inputs)
            )
        )

    def data_type_group(self):
        return self.get_group(
            lambda inputs: list(
                map(dataset.get_data_type, inputs)
            )
        )
