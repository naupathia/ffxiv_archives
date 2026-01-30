from functools import wraps
import time

import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.INFO)

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        LOGGER.debug(f'ELAPSED TIME: {func.__name__} took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

class Timer:

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start_time = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.perf_counter()
        total_time = end_time - self.start_time
        LOGGER.debug(f'ELAPSED TIME: {self.name} took {total_time:.4f} seconds')