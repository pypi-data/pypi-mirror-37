from dask import delayed
from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler,\
    visualize, ProgressBar
import dask


class ForLoop:
    def __init__(self, inputs, func, merge_func=None, **kwargs):
        results = []
        for data in inputs:
            result = func(data, **kwargs)
            results.append(result)
        if merge_func is not None:
            self._result = merge_func(results, **kwargs)
        else:
            self._result = results

    def compute(self, **kwargs):
        with Profiler() as prof, ResourceProfiler(dt=0.25) as rprof, CacheProfiler() as cprof:
            self._computed_result = dask.compute(self._result, **kwargs)[0]
            self._prof = prof
            self._rprof = rprof
            self._cprof = cprof

    def show_profiling(self, output_filepath=None):
        visualize([self._prof, self._rprof, self._cprof],
                  file_path=output_filepath)

    def show_workflow(self, output_filepath=None):
        dask.visualize(self._result, filename=output_filepath)

    def get_result(self):
        return self._computed_result
