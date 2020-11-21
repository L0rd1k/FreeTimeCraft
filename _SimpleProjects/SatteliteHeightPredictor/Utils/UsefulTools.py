import time

def timer(func):
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # starts running
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  #  function finishes
        run_time = end_time - start_time  # difference
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer