from multiprocessing.pool import ThreadPool
from threading import Thread


class ResponseThread(Thread):

    result = None

    def __init__(self, func_args=None, func_kwargs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._func_args = func_args
        self._func_kwargs = func_kwargs

    def run(self):
        try:
            if hasattr(self, "_target") and self._target:
                self.result = (self._target(*self._func_args, **self._func_kwargs), None)

        except Exception as e:
            self.result = (None, e)

    def join(self, **kwargs):
        Thread.join(self, **kwargs)
        return self.result


def thread(func):
    def wrapper(*args, **kwargs):

        t = ResponseThread(func_args=args, func_kwargs=kwargs, target=func)
        t.start()

        return t
    return wrapper


def parallel(n_threads=None, n_thread_max=256, chunk_count=None):
    def parallel_decorator(func):
        def wrapper(iterable_values):

            pool_size = n_threads if n_threads is not None else min(len(iterable_values), n_thread_max)
            p = ThreadPool(pool_size)
            result = p.map(func, iterable_values, chunk_count)
            p.close()

            return result
        return wrapper
    return parallel_decorator
