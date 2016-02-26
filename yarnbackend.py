from sklearn.externals.joblib._parallel_backends import ThreadingBackend
from sklearn.externals.joblib.my_exceptions import WorkerInterrupt
from yarnpool import YarnPool

class YarnBackend(ThreadingBackend):

    def effective_n_jobs(self, n_jobs):
        # TODO: add support -1, -2 etc.
        if n_jobs < 0:
            raise ValueError('n_jobs < 0 is not implemented yet')

        return n_jobs

    def initialize(self, n_jobs, poolargs):
        self._pool = YarnPool(n_jobs)
        return n_jobs

    def get_exceptions(self):
        # We are using multiprocessing, we also want to capture
        # KeyboardInterrupts
        return [KeyboardInterrupt, WorkerInterrupt]
