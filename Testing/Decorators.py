import time
from dataclasses import dataclass

def my_decorator(func):
    def my_wrapper(*args, **kwargs):
        print("Wrapper {}!".format(*args, **kwargs))
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return my_wrapper

def timer_decorator(func):
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # starts running
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  #  function finishes
        run_time = end_time - start_time  # difference
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

PLUGINS = dict()
def register_decorator(func):
    PLUGINS[func.__name__] = func
    return func

# ==========================================================================


#@timer_decorator
@register_decorator
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])

''' EXAMPLE OF NESTING DECORATORS (apply several decorators) '''
#@register_decorator
@my_decorator
@timer_decorator
def hello_world(value):
    print("{}".format(value))

hello_world("Check state")

@my_decorator
@register_decorator
def say_whee(name):
    print("Test decorator value = {}".format(name))
    return "Return value = {}".format(name)

#print(PLUGINS)

''' CLASS DECORATOR's EXAMPLES '''
''' 1) DECORATE THE METHODS OF A CLASS '''
class TimeWaster:
    @timer_decorator
    def waste_time(self, num_times):
        for _ in range(num_times):
            sum([i ** 2 for i in range(10000)])
#tw = TimeWaster()
#tw.waste_time(10)
''' 2) DECORATE THE WHOLE CLASS '''
@timer_decorator
class TimeWasterSecond:
    def waste_time(self, num_times):
        for _ in range(num_times):
            sum([i**2 for i in range(10000)])

#tw = TimeWasterSecond()
#tw.waste_time(10)
''' 3) DECORATORS WITH ARGUMENTS '''
def repeat_decorator(num_times):
    def decorator_repeat(func):
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return decorator_repeat

@repeat_decorator(num_times=4)
def repeat_function(value):
    print(f"Just {value}")

repeat_function("Repeat")

''' DECORATOR WITH AND WITHOUT ARGUMENTS '''
def repeate_decorator_second(_func=None, *, num_times=2):
    def decorator_repeat(func):
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    if _func is None:
        return decorator_repeat
    else:
        return decorator_repeat(_func)

@repeate_decorator_second
# @repeate_decorator_second(num_times = 5)
def repeat_function(value):
    print(f"Just {value} second")

''' STATEFUL DECORATORS - a decorator that can keep track of state '''
def count_calls(func):
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls

@repeat_decorator(num_times=4)
@count_calls
def say_whee():
    print("Whee!")

say_whee()

"""Make a class a Singleton class (only one instance)"""
def singleton(cls):
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton

@singleton
class TheOne:
    pass

first_one = TheOne()
another_one = TheOne()
print("Singletone decorator: {}".format(first_one is another_one))

""" Keep a cache of previous function calls. You can use @functools.lru_cache"""
def cache(func):
    def wrapper_cache(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key not in wrapper_cache.cache:
            wrapper_cache.cache[cache_key] = func(*args, **kwargs)
        return wrapper_cache.cache[cache_key]
    wrapper_cache.cache = dict()
    return wrapper_cache

@cache
@count_calls
def fibonacci(num):
    if num < 2:
        return num
    return fibonacci(num - 1) + fibonacci(num - 2)

print("Fibonacci: {}".format(fibonacci(10)))