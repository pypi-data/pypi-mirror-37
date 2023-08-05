from dask import delayed
from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler,\
    visualize, ProgressBar
import dask


class ForLoop:
    def __init__(self, func, merge_func, inputs, **kwargs):
        results = []
        for data in inputs:
            result = delayed(func)(data, **kwargs)
            results.append(result)
        self._result = delayed(merge_func)(results)

    def compute(self):
        with Profiler() as prof, ResourceProfiler(dt=0.25) as rprof, CacheProfiler() as cprof, ProgressBar():
            self._result = self._result.compute()
            self._prof = prof
            self._rprof = rprof
            self._cprof = cprof

    def show_profiling(self, output_filepath=None):
        visualize([self._prof, self._rprof, self._cprof],
                  file_path=output_filepath)

    def get_result(self):
        return self._result
